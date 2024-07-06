# NB these tests are intended to check whether the python bindings are
# working, not whether libxkbcommon itself is working!

from unittest import TestCase

from xkbcommon import xkb

from tests.data import sample_keymap_string, sample_keymap_bytes, \
    sample_compose_bytes

import os
import tempfile
from io import BytesIO
import array

# A directory that is guaranteed to exist
testdir = os.path.dirname(os.path.abspath(__file__))
# A path that is guaranteed not to exist
nonexistent = os.path.join(testdir, "must-not-exist")
# A file that is guaranteed to exist
testfile = os.path.abspath(__file__)


class TestKeysym(TestCase):
    def test_keysym_get_name(self):
        self.assertEqual(xkb.keysym_get_name(0xff68), "Find")

    def test_keysym_from_name(self):
        self.assertEqual(xkb.keysym_from_name("space"), 0x20)

    def test_keysym_to_string(self):
        self.assertEqual(xkb.keysym_to_string(0x20), ' ')

    def test_keysym_to_upper(self):
        # Lower case to upper case A
        self.assertEqual(xkb.keysym_to_upper(0x61), 0x41)

    def test_keysym_to_lower(self):
        # Upper case to lower case A
        self.assertEqual(xkb.keysym_to_lower(0x41), 0x61)


class TestContext(TestCase):
    @classmethod
    def setUpClass(cls):
        # Create temporary files to use while testing.
        cls._sample_keymap_file = tempfile.NamedTemporaryFile(
            mode='w+b')
        cls._sample_keymap_file.write(sample_keymap_bytes)
        cls._sample_compose_file = tempfile.NamedTemporaryFile(
            mode='w+b')
        cls._sample_compose_file.write(sample_compose_bytes)

    @classmethod
    def tearDownClass(cls):
        cls._sample_keymap_file.close()
        cls._sample_compose_file.close()

    def test_create(self):
        xkb.Context()

    def test_default_includes(self):
        ctx = xkb.Context(no_default_includes=True)
        self.assertEqual(len(list(ctx.include_path())), 0)

    def test_include_path_append_exists(self):
        ctx = xkb.Context()
        ctx.include_path_append(testdir)
        self.assertIn(testdir, ctx.include_path())

    def test_include_path_append_file(self):
        ctx = xkb.Context()
        with self.assertRaises(xkb.XKBPathError):
            ctx.include_path_append(testfile)
        self.assertNotIn(testfile, ctx.include_path())

    def test_include_path_append_does_not_exist(self):
        ctx = xkb.Context()
        with self.assertRaises(xkb.XKBPathError):
            ctx.include_path_append(nonexistent)
        self.assertNotIn(nonexistent, ctx.include_path())

    def test_num_include_paths(self):
        ctx = xkb.Context()
        default_num_include_paths = ctx.num_include_paths()
        ctx.include_path_append(testdir)
        self.assertEqual(ctx.num_include_paths(),
                         default_num_include_paths + 1)

    def test_set_log_level(self):
        ctx = xkb.Context()
        self.assertEqual(ctx.get_log_level(), xkb.lib.XKB_LOG_LEVEL_ERROR)
        ctx.set_log_level(xkb.lib.XKB_LOG_LEVEL_DEBUG)
        self.assertEqual(ctx.get_log_level(), xkb.lib.XKB_LOG_LEVEL_DEBUG)

    def test_set_log_verbosity(self):
        ctx = xkb.Context()
        self.assertEqual(ctx.get_log_verbosity(), 0)
        ctx.set_log_verbosity(10)
        self.assertEqual(ctx.get_log_verbosity(), 10)

    def test_set_log_handler(self):
        messages = []

        def handler(context, level, message):
            messages.append(message)

        ctx = xkb.Context()
        ctx.set_log_level(xkb.lib.XKB_LOG_LEVEL_DEBUG)
        ctx.set_log_verbosity(10)
        ctx.set_log_fn(handler)
        ctx.keymap_new_from_string(sample_keymap_string)
        self.assertNotEqual(len(messages), 0)

    def test_keymap_new_from_names_with_args(self):
        # NB this test requires that suitable keymaps are installed
        # wherever xkbcommon expects to find them
        ctx = xkb.Context(no_environment_names=True)
        km = ctx.keymap_new_from_names(
            rules="evdev", model="pc105", layout="gb",
            variant="dvorak", options="terminate:ctrl_alt_bksp")
        self.assertIsNotNone(km)

    def test_keymap_new_from_names(self):
        ctx = xkb.Context()
        km = ctx.keymap_new_from_names()
        self.assertIsNotNone(km)

    def test_keymap_new_from_file_mmap(self):
        ctx = xkb.Context()
        self._sample_keymap_file.seek(0)
        km = ctx.keymap_new_from_file(self._sample_keymap_file)
        self.assertIsNotNone(km, None)
        self.assertEqual(km.load_method, "mmap_file")

    def test_keymap_new_from_file_no_mmap(self):
        ctx = xkb.Context()
        memfile = BytesIO(sample_keymap_bytes)
        km = ctx.keymap_new_from_file(memfile)
        self.assertIsNotNone(km)
        self.assertEqual(km.load_method, "read_file")

    def test_keymap_new_from_string(self):
        ctx = xkb.Context()
        km = ctx.keymap_new_from_string(sample_keymap_string)
        self.assertIsNotNone(km, None)
        self.assertEqual(km.load_method, "string")

    def test_keymap_new_from_buffer(self):
        ctx = xkb.Context()
        test_data = array.array('b', sample_keymap_bytes)
        km = ctx.keymap_new_from_buffer(test_data)
        self.assertIsNotNone(km)
        self.assertEqual(km.load_method, "buffer")
        test_data.extend([0] * 10)
        length = len(sample_keymap_bytes)
        km = ctx.keymap_new_from_buffer(test_data, length=length)
        self.assertIsNotNone(km)

    def test_compose_table_new_from_locale(self):
        ctx = xkb.Context()
        ct = ctx.compose_table_new_from_locale("en_GB.UTF-8")
        self.assertIsNotNone(ct)
        self.assertEqual(ct.load_method, "locale")

    def test_compose_table_new_from_locale_fail(self):
        ctx = xkb.Context()
        with self.assertRaises(xkb.XKBComposeTableCreationFailure):
            ctx.compose_table_new_from_locale("not-a-locale")

    def test_compose_table_new_from_file_mmap(self):
        ctx = xkb.Context()
        self._sample_compose_file.seek(0)
        ct = ctx.compose_table_new_from_file(
            self._sample_compose_file, "en_US.UTF-8")
        self.assertIsNotNone(ct)
        self.assertEqual(ct.load_method, "mmap_file")

    def test_compose_table_new_from_file_no_mmap(self):
        ctx = xkb.Context()
        memfile = BytesIO(sample_compose_bytes)
        ct = ctx.compose_table_new_from_file(memfile, "en_US.UTF-8")
        self.assertIsNotNone(ct)
        self.assertEqual(ct.load_method, "read_file")

    def test_compose_table_new_from_buffer(self):
        ctx = xkb.Context()
        test_data = sample_compose_bytes
        ct = ctx.compose_table_new_from_buffer(test_data, "en_US.UTF-8")
        self.assertIsNotNone(ct)
        self.assertEqual(ct.load_method, "buffer")


# This class makes use of the details of the sample keymap in
# sample_keymap_string.
class TestKeymap(TestCase):
    @classmethod
    def setUpClass(cls):
        cls._ctx = xkb.Context()
        cls.km = cls._ctx.keymap_new_from_string(sample_keymap_string)

    def test_keymap_get_as_string(self):
        kms = self.km.get_as_string()
        self.assertNotEqual(len(kms), 0)

    def test_keymap_min_keycode(self):
        self.assertEqual(self.km.min_keycode(), 9)

    def test_keymap_max_keycode(self):
        self.assertEqual(self.km.max_keycode(), 253)

    def test_keymap_iterate_over_keycodes(self):
        self.assertEqual(len(list(self.km)), 245)

    def test_keymap_key_names_roundtrip(self):
        # Test both key_get_name() and key_by_name()
        for keycode in iter(self.km):
            try:
                name = self.km.key_get_name(keycode)
                self.assertEqual(self.km.key_by_name(name), keycode)
            except xkb.XKBInvalidKeycode:
                pass

    def test_keymap_key_get_name_invalid(self):
        # Keycode 93 does not exist in our sample keymap
        with self.assertRaises(xkb.XKBInvalidKeycode):
            self.km.key_get_name(93)

    def test_keymap_key_by_name_invalid(self):
        # Keycode 'WIBL' does not exist in our sample keymap
        with self.assertRaises(xkb.XKBKeyDoesNotExist):
            self.km.key_by_name("WIBL")

    def test_keymap_num_mods(self):
        self.assertEqual(self.km.num_mods(), 21)

    def test_keymap_mod_get_name(self):
        self.assertEqual(self.km.mod_get_name(0), "Shift")

    def test_keymap_mod_get_name_fail(self):
        with self.assertRaises(xkb.XKBInvalidModifierIndex):
            self.km.mod_get_name(self.km.num_mods())

    def test_keymap_mod_get_index(self):
        self.assertEqual(self.km.mod_get_index("Shift"), 0)

    def test_keymap_mod_get_index_fail(self):
        with self.assertRaises(xkb.XKBModifierDoesNotExist):
            self.km.mod_get_index("wibble")

    def test_keymap_num_layouts(self):
        self.assertEqual(self.km.num_layouts(), 2)

    def test_keymap_layout_get_name(self):
        self.assertEqual(self.km.layout_get_name(0), "English (UK)")

    def test_keymap_layout_get_name_fail(self):
        with self.assertRaises(xkb.XKBInvalidLayoutIndex):
            self.km.layout_get_name(self.km.num_layouts())

    def test_keymap_layout_get_index(self):
        self.assertEqual(self.km.layout_get_index("English (UK)"), 0)

    def test_keymap_layout_get_index_fail(self):
        with self.assertRaises(xkb.XKBLayoutDoesNotExist):
            self.km.layout_get_index("wibble")

    def test_keymap_num_leds(self):
        self.assertEqual(self.km.num_leds(), 14)

    def test_keymap_led_get_name(self):
        self.assertEqual(self.km.led_get_name(0), "Caps Lock")

    def test_keymap_led_get_name_fail(self):
        with self.assertRaises(xkb.XKBInvalidLEDIndex):
            self.km.led_get_name(self.km.num_leds())

    def test_keymap_led_get_index(self):
        self.assertEqual(self.km.led_get_index("Caps Lock"), 0)

    def test_keymap_led_get_index_fail(self):
        with self.assertRaises(xkb.XKBLEDDoesNotExist):
            self.km.led_get_index("wibble")

    def test_keymap_num_layouts_for_key(self):
        key = next(iter(self.km))
        self.assertEqual(self.km.num_layouts_for_key(key), 1)

    def test_keymap_num_levels_for_key(self):
        key = next(iter(self.km))
        self.assertEqual(self.km.num_levels_for_key(key, 0), 1)

    def test_keymap_key_get_mods_for_level(self):
        first_invalid_mask = 1 << self.km.num_mods()
        for key in self.km:
            for layout in range(self.km.num_layouts_for_key(key)):
                for level in range(self.km.num_levels_for_key(key, layout)):
                    r = self.km.key_get_mods_for_level(key, layout, level)
                    for mm in r:
                        self.assertLess(mm, first_invalid_mask)

    def test_keymap_key_get_syms_by_level(self):
        for key in self.km:
            r = self.km.key_get_syms_by_level(key, 0, 0)
            for k in r:
                # If we are returned an invalid keysym, this will raise
                # XKBInvalidKeysym
                self.assertTrue(xkb.keysym_get_name(k))

    def test_keymap_key_repeats(self):
        key = next(iter(self.km))
        self.assertEqual(self.km.key_repeats(key), True)

    def test_keymap_state_new(self):
        self.assertIsNotNone(self.km.state_new())


class TestBitEnum(TestCase):
    def test_StateComponent(self):
        a = xkb.XKB_STATE_MODS_DEPRESSED
        b = xkb.XKB_STATE_MODS_LATCHED
        self.assertIsInstance(a | b, xkb.StateComponent)

        # The order in which enum members are listed is implementation
        # defined and does in practice vary between different Python
        # versions. Both possibilities should be acceptable.

        self.assertIn(
            str(a | b),
            ("StateComponent.XKB_STATE_MODS_LATCHED|XKB_STATE_MODS_DEPRESSED",
             "StateComponent.XKB_STATE_MODS_DEPRESSED|XKB_STATE_MODS_LATCHED"))
        c = a | 0x1000000
        self.assertIn(
            str(c),
            ("StateComponent.16777216|XKB_STATE_MODS_DEPRESSED",
             "StateComponent.XKB_STATE_MODS_DEPRESSED|16777216"))

    def test_StateMatch(self):
        self.assertIn(
            str(xkb.XKB_STATE_MATCH_ANY | xkb.XKB_STATE_MATCH_ALL),
            ("StateMatch.XKB_STATE_MATCH_ALL|XKB_STATE_MATCH_ANY",
             "StateMatch.XKB_STATE_MATCH_ANY|XKB_STATE_MATCH_ALL"))


class TestKeyboardState(TestCase):
    capslock = 66
    space = 65

    @classmethod
    def setUpClass(cls):
        cls._ctx = xkb.Context()
        cls.km = cls._ctx.keymap_new_from_string(sample_keymap_string)
        cls.lock = cls.km.mod_get_index("Lock")
        cls.numlock = cls.km.mod_get_index("NumLock")
        cls.badmod = cls.km.num_mods()

    def test_state_get_keymap(self):
        state = self.km.state_new()
        self.assertEqual(state.get_keymap(), self.km)
        self.assertEqual(state.keymap, self.km)

    def test_state_update_key(self):
        state = self.km.state_new()
        self.assertEqual(
            state.mod_name_is_active("Lock", xkb.XKB_STATE_MODS_LOCKED),
            False)
        keydown = state.update_key(self.capslock, xkb.XKB_KEY_DOWN)
        self.assertEqual(
            keydown, xkb.XKB_STATE_LEDS | xkb.XKB_STATE_MODS_EFFECTIVE
            | xkb.XKB_STATE_MODS_LOCKED | xkb.XKB_STATE_MODS_DEPRESSED)
        self.assertIsInstance(keydown, xkb.StateComponent)
        self.assertIsInstance(keydown, int)
        keyup = state.update_key(self.capslock, xkb.XKB_KEY_UP)
        self.assertEqual(
            keyup, xkb.XKB_STATE_MODS_DEPRESSED)
        self.assertEqual(
            state.mod_name_is_active("Lock", xkb.XKB_STATE_MODS_LOCKED),
            True)

    def test_state_update_mask(self):
        master_state = self.km.state_new()
        slave_state = self.km.state_new()
        master_state.update_key(self.capslock, xkb.XKB_KEY_DOWN)
        master_state.update_key(self.capslock, xkb.XKB_KEY_UP)
        depressed_mods = master_state.serialize_mods(
            xkb.XKB_STATE_MODS_DEPRESSED)
        latched_mods = master_state.serialize_mods(
            xkb.XKB_STATE_MODS_LATCHED)
        locked_mods = master_state.serialize_mods(
            xkb.XKB_STATE_MODS_LOCKED)
        depressed_layout = master_state.serialize_layout(
            xkb.XKB_STATE_LAYOUT_DEPRESSED)
        latched_layout = master_state.serialize_layout(
            xkb.XKB_STATE_LAYOUT_LATCHED)
        locked_layout = master_state.serialize_layout(
            xkb.XKB_STATE_LAYOUT_LOCKED)
        self.assertEqual(
            slave_state.mod_name_is_active("Lock", xkb.XKB_STATE_MODS_LOCKED),
            False)
        r = slave_state.update_mask(
            depressed_mods, latched_mods, locked_mods,
            depressed_layout, latched_layout, locked_layout)
        self.assertIsInstance(r, int)
        self.assertIsInstance(r, xkb.StateComponent)
        self.assertEqual(
            r, xkb.XKB_STATE_LEDS | xkb.XKB_STATE_MODS_EFFECTIVE
            | xkb.XKB_STATE_MODS_LOCKED)
        self.assertEqual(
            slave_state.mod_name_is_active("Lock", xkb.XKB_STATE_MODS_LOCKED),
            True)

    def test_state_key_get_syms(self):
        state = self.km.state_new()
        syms = state.key_get_syms(self.space)
        self.assertEqual(syms, [32])

    def test_state_ket_get_string(self):
        state = self.km.state_new()
        self.assertEqual(state.key_get_string(self.capslock), "")
        self.assertEqual(state.key_get_string(self.space), " ")

    def test_state_key_get_one_sym(self):
        state = self.km.state_new()
        self.assertEqual(state.key_get_one_sym(self.capslock), 65509)
        self.assertEqual(state.key_get_one_sym(self.space), 32)

    def test_state_key_get_layout(self):
        state = self.km.state_new()
        self.assertEqual(state.key_get_layout(self.space), 0)

    def test_state_key_get_layout_fail(self):
        state = self.km.state_new()
        with self.assertRaises(xkb.XKBInvalidLayoutIndex):
            state.key_get_layout(0)

    def test_state_key_get_level(self):
        state = self.km.state_new()
        self.assertEqual(state.key_get_level(self.space, 0), 0)

    def test_state_key_get_level_fail(self):
        state = self.km.state_new()
        with self.assertRaises(xkb.XKBInvalidLayoutIndex):
            state.key_get_level(0, 0)

    # serialize_mods and serialize_layout are tested in test_state_update_mask

    # mod_name_is_active is tested in test_state_update_key

    def test_state_mod_names_are_active(self):
        state = self.km.state_new()
        self.assertFalse(
            state.mod_names_are_active(xkb.XKB_STATE_MODS_LOCKED,
                                       xkb.XKB_STATE_MATCH_ANY,
                                       ["Lock", "NumLock"]))
        state.update_key(self.capslock, xkb.XKB_KEY_DOWN)
        state.update_key(self.capslock, xkb.XKB_KEY_UP)
        self.assertTrue(
            state.mod_names_are_active(xkb.XKB_STATE_MODS_LOCKED,
                                       xkb.XKB_STATE_MATCH_ANY,
                                       ["Lock", "NumLock"]))

    def test_state_mod_index_is_active(self):
        state = self.km.state_new()
        self.assertFalse(
            state.mod_index_is_active(self.lock, xkb.XKB_STATE_MODS_LOCKED))
        state.update_key(self.capslock, xkb.XKB_KEY_DOWN)
        state.update_key(self.capslock, xkb.XKB_KEY_UP)
        self.assertTrue(
            state.mod_index_is_active(self.lock, xkb.XKB_STATE_MODS_LOCKED))

    def test_state_mod_index_is_active_fail(self):
        state = self.km.state_new()
        with self.assertRaises(xkb.XKBInvalidModifierIndex):
            state.mod_index_is_active(self.badmod,
                                      xkb.XKB_STATE_MODS_LOCKED)

    def test_state_mod_indices_are_active(self):
        state = self.km.state_new()
        self.assertFalse(
            state.mod_indices_are_active(xkb.XKB_STATE_MODS_LOCKED,
                                         xkb.XKB_STATE_MATCH_ANY,
                                         [self.lock, self.numlock]))
        state.update_key(self.capslock, xkb.XKB_KEY_DOWN)
        state.update_key(self.capslock, xkb.XKB_KEY_UP)
        self.assertTrue(
            state.mod_indices_are_active(xkb.XKB_STATE_MODS_LOCKED,
                                         xkb.XKB_STATE_MATCH_ANY,
                                         [self.lock, self.numlock]))

    def test_state_mod_indices_are_active_fail(self):
        state = self.km.state_new()
        with self.assertRaises(xkb.XKBInvalidModifierIndex):
            state.mod_indices_are_active(xkb.XKB_STATE_MODS_LOCKED,
                                         xkb.XKB_STATE_MATCH_ANY,
                                         [self.badmod])

    def test_state_mod_index_is_consumed(self):
        state = self.km.state_new()
        self.assertIsInstance(
            state.mod_index_is_consumed(self.space, self.lock),
            bool)

    def test_state_mod_index_is_consumed_fail(self):
        state = self.km.state_new()
        with self.assertRaises(xkb.XKBInvalidModifierIndex):
            state.mod_index_is_consumed(self.space, self.badmod)

    def test_state_mod_mask_remove_consumed(self):
        state = self.km.state_new()
        self.assertEqual(
            state.mod_mask_remove_consumed(self.space, 0), 0)

    def test_state_key_get_consumed_mods(self):
        state = self.km.state_new()
        self.assertEqual(
            state.key_get_consumed_mods(self.space), 0)

    def test_state_layout_name_is_active(self):
        state = self.km.state_new()
        self.assertTrue(
            state.layout_name_is_active("English (UK)",
                                        xkb.XKB_STATE_LAYOUT_EFFECTIVE))

    def test_state_layout_name_is_active_fail(self):
        state = self.km.state_new()
        with self.assertRaises(xkb.XKBLayoutDoesNotExist):
            state.layout_name_is_active("wibble",
                                        xkb.XKB_STATE_LAYOUT_EFFECTIVE)

    def test_state_layout_index_is_active(self):
        state = self.km.state_new()
        self.assertTrue(
            state.layout_index_is_active(0, xkb.XKB_STATE_LAYOUT_EFFECTIVE))

    def test_state_layout_index_is_active_fail(self):
        state = self.km.state_new()
        with self.assertRaises(xkb.XKBInvalidLayoutIndex):
            state.layout_index_is_active(self.km.num_layouts(),
                                         xkb.XKB_STATE_LAYOUT_EFFECTIVE)

    def test_state_led_name_is_active(self):
        state = self.km.state_new()
        self.assertFalse(state.led_name_is_active("Caps Lock"))
        state.update_key(self.capslock, xkb.XKB_KEY_DOWN)
        state.update_key(self.capslock, xkb.XKB_KEY_UP)
        self.assertTrue(state.led_name_is_active("Caps Lock"))

    def test_state_led_name_is_active_fail(self):
        state = self.km.state_new()
        with self.assertRaises(xkb.XKBLEDDoesNotExist):
            state.led_name_is_active("wibble")

    def test_state_led_index_is_active(self):
        state = self.km.state_new()
        capslockled = self.km.led_get_index("Caps Lock")
        self.assertFalse(state.led_index_is_active(capslockled))
        state.update_key(self.capslock, xkb.XKB_KEY_DOWN)
        state.update_key(self.capslock, xkb.XKB_KEY_UP)
        self.assertTrue(state.led_index_is_active(capslockled))

    def test_state_led_index_is_active_fail(self):
        state = self.km.state_new()
        with self.assertRaises(xkb.XKBInvalidLEDIndex):
            state.led_index_is_active(self.km.num_leds())


class TestComposeTable(TestCase):
    @classmethod
    def setUpClass(cls):
        ctx = xkb.Context()
        cls.ct = ctx.compose_table_new_from_buffer(
            sample_compose_bytes, "en_US.UTF-8")

    def test_compose_table_create_compose_state(self):
        state = self.ct.compose_state_new()
        self.assertIsInstance(state, xkb.ComposeState)


class TestCompose(TestCase):
    XKB_KEYSYM_OHORNTILDE = 0x1001ee0
    UTF8_OHORNTILDE = "Ỡ"

    XKB_KEYSYM_DEAD_CIRCUMFLEX = 0xfe52
    UTF_CIRCUMFLEX = "^"

    XKB_KEYSYM_DEAD_TILDE = 0xfe53
    XKB_KEYSYM_DEAD_HORN = 0xfe62
    XKB_KEYSYM_O = 0x004f
    XKB_KEYSYM_F = 0x0066

    @classmethod
    def setUpClass(cls):
        ctx = xkb.Context()
        ct = ctx.compose_table_new_from_buffer(
            sample_compose_bytes, "en_US.UTF-8")
        cls.compose = ct.compose_state_new()

    def test_compose_initial_status(self):
        self.compose.reset()
        self.assertEqual(
            self.compose.get_status(),
            xkb.ComposeStatus.XKB_COMPOSE_NOTHING
        )

    def test_compose_feed_double_dead_circumflex(self):
        self.compose.reset()

        self.assertEqual(
            self.compose.feed(self.XKB_KEYSYM_DEAD_CIRCUMFLEX),
            xkb.ComposeFeedResult.XKB_COMPOSE_FEED_ACCEPTED
        )
        self.assertEqual(
            self.compose.get_status(),
            xkb.ComposeStatus.XKB_COMPOSE_COMPOSING
        )

        self.assertEqual(
            self.compose.feed(self.XKB_KEYSYM_DEAD_CIRCUMFLEX),
            xkb.ComposeFeedResult.XKB_COMPOSE_FEED_ACCEPTED
        )

        self.assertEqual(
            self.compose.get_status(),
            xkb.ComposeStatus.XKB_COMPOSE_COMPOSED
        )
        self.assertEqual(self.compose.get_utf8(), self.UTF_CIRCUMFLEX)

    def test_compose_feed_non_composing(self):
        self.compose.reset()

        self.assertEqual(
            self.compose.feed(self.XKB_KEYSYM_DEAD_TILDE),
            xkb.ComposeFeedResult.XKB_COMPOSE_FEED_ACCEPTED
        )
        self.assertEqual(
            self.compose.feed(self.XKB_KEYSYM_F),
            xkb.ComposeFeedResult.XKB_COMPOSE_FEED_ACCEPTED
        )
        self.assertEqual(
            self.compose.get_status(), xkb.ComposeStatus.XKB_COMPOSE_CANCELLED
        )

        self.assertEqual(
            self.compose.feed(self.XKB_KEYSYM_F),
            xkb.ComposeFeedResult.XKB_COMPOSE_FEED_ACCEPTED
        )
        self.assertEqual(
            self.compose.get_status(), xkb.ComposeStatus.XKB_COMPOSE_NOTHING
        )

    def test_compose_feed_multi_composing(self):
        self.compose.reset()

        self.assertEqual(
            self.compose.feed(self.XKB_KEYSYM_DEAD_TILDE),
            xkb.ComposeFeedResult.XKB_COMPOSE_FEED_ACCEPTED
        )
        self.assertEqual(
            self.compose.feed(self.XKB_KEYSYM_DEAD_HORN),
            xkb.ComposeFeedResult.XKB_COMPOSE_FEED_ACCEPTED
        )
        self.assertEqual(
            self.compose.feed(self.XKB_KEYSYM_O),
            xkb.ComposeFeedResult.XKB_COMPOSE_FEED_ACCEPTED
        )
        self.assertEqual(
            self.compose.get_status(), xkb.ComposeStatus.XKB_COMPOSE_COMPOSED
        )
        self.assertEqual(self.compose.get_utf8(), self.UTF8_OHORNTILDE)
        self.assertEqual(self.compose.get_one_sym(), self.XKB_KEYSYM_OHORNTILDE)
