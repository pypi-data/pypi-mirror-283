# Defines sample_keymap_string, sample_keymap_bytes and sample_compose_bytes

# This sample keymap is the output of xkbcomp :0 [filename] on my
# system - it wasn't chosen for any other reason.  Some of the tests
# may rely on its details.

sample_keymap_string = r"""
xkb_keymap {
xkb_keycodes "evdev+aliases(qwerty)" {
    minimum = 8;
    maximum = 255;
     <ESC> = 9;
    <AE01> = 10;
    <AE02> = 11;
    <AE03> = 12;
    <AE04> = 13;
    <AE05> = 14;
    <AE06> = 15;
    <AE07> = 16;
    <AE08> = 17;
    <AE09> = 18;
    <AE10> = 19;
    <AE11> = 20;
    <AE12> = 21;
    <BKSP> = 22;
     <TAB> = 23;
    <AD01> = 24;
    <AD02> = 25;
    <AD03> = 26;
    <AD04> = 27;
    <AD05> = 28;
    <AD06> = 29;
    <AD07> = 30;
    <AD08> = 31;
    <AD09> = 32;
    <AD10> = 33;
    <AD11> = 34;
    <AD12> = 35;
    <RTRN> = 36;
    <LCTL> = 37;
    <AC01> = 38;
    <AC02> = 39;
    <AC03> = 40;
    <AC04> = 41;
    <AC05> = 42;
    <AC06> = 43;
    <AC07> = 44;
    <AC08> = 45;
    <AC09> = 46;
    <AC10> = 47;
    <AC11> = 48;
    <TLDE> = 49;
    <LFSH> = 50;
    <BKSL> = 51;
    <AB01> = 52;
    <AB02> = 53;
    <AB03> = 54;
    <AB04> = 55;
    <AB05> = 56;
    <AB06> = 57;
    <AB07> = 58;
    <AB08> = 59;
    <AB09> = 60;
    <AB10> = 61;
    <RTSH> = 62;
    <KPMU> = 63;
    <LALT> = 64;
    <SPCE> = 65;
    <CAPS> = 66;
    <FK01> = 67;
    <FK02> = 68;
    <FK03> = 69;
    <FK04> = 70;
    <FK05> = 71;
    <FK06> = 72;
    <FK07> = 73;
    <FK08> = 74;
    <FK09> = 75;
    <FK10> = 76;
    <NMLK> = 77;
    <SCLK> = 78;
     <KP7> = 79;
     <KP8> = 80;
     <KP9> = 81;
    <KPSU> = 82;
     <KP4> = 83;
     <KP5> = 84;
     <KP6> = 85;
    <KPAD> = 86;
     <KP1> = 87;
     <KP2> = 88;
     <KP3> = 89;
     <KP0> = 90;
    <KPDL> = 91;
    <LVL3> = 92;
    <LSGT> = 94;
    <FK11> = 95;
    <FK12> = 96;
    <AB11> = 97;
    <KATA> = 98;
    <HIRA> = 99;
    <HENK> = 100;
    <HKTG> = 101;
    <MUHE> = 102;
    <JPCM> = 103;
    <KPEN> = 104;
    <RCTL> = 105;
    <KPDV> = 106;
    <PRSC> = 107;
    <RALT> = 108;
    <LNFD> = 109;
    <HOME> = 110;
      <UP> = 111;
    <PGUP> = 112;
    <LEFT> = 113;
    <RGHT> = 114;
     <END> = 115;
    <DOWN> = 116;
    <PGDN> = 117;
     <INS> = 118;
    <DELE> = 119;
    <I120> = 120;
    <MUTE> = 121;
    <VOL-> = 122;
    <VOL+> = 123;
    <POWR> = 124;
    <KPEQ> = 125;
    <I126> = 126;
    <PAUS> = 127;
    <I128> = 128;
    <I129> = 129;
    <HNGL> = 130;
    <HJCV> = 131;
    <AE13> = 132;
    <LWIN> = 133;
    <RWIN> = 134;
    <COMP> = 135;
    <STOP> = 136;
    <AGAI> = 137;
    <PROP> = 138;
    <UNDO> = 139;
    <FRNT> = 140;
    <COPY> = 141;
    <OPEN> = 142;
    <PAST> = 143;
    <FIND> = 144;
     <CUT> = 145;
    <HELP> = 146;
    <I147> = 147;
    <I148> = 148;
    <I149> = 149;
    <I150> = 150;
    <I151> = 151;
    <I152> = 152;
    <I153> = 153;
    <I154> = 154;
    <I155> = 155;
    <I156> = 156;
    <I157> = 157;
    <I158> = 158;
    <I159> = 159;
    <I160> = 160;
    <I161> = 161;
    <I162> = 162;
    <I163> = 163;
    <I164> = 164;
    <I165> = 165;
    <I166> = 166;
    <I167> = 167;
    <I168> = 168;
    <I169> = 169;
    <I170> = 170;
    <I171> = 171;
    <I172> = 172;
    <I173> = 173;
    <I174> = 174;
    <I175> = 175;
    <I176> = 176;
    <I177> = 177;
    <I178> = 178;
    <I179> = 179;
    <I180> = 180;
    <I181> = 181;
    <I182> = 182;
    <I183> = 183;
    <I184> = 184;
    <I185> = 185;
    <I186> = 186;
    <I187> = 187;
    <I188> = 188;
    <I189> = 189;
    <I190> = 190;
    <FK13> = 191;
    <FK14> = 192;
    <FK15> = 193;
    <FK16> = 194;
    <FK17> = 195;
    <FK18> = 196;
    <FK19> = 197;
    <FK20> = 198;
    <FK21> = 199;
    <FK22> = 200;
    <FK23> = 201;
    <FK24> = 202;
    <MDSW> = 203;
     <ALT> = 204;
    <META> = 205;
    <SUPR> = 206;
    <HYPR> = 207;
    <I208> = 208;
    <I209> = 209;
    <I210> = 210;
    <I211> = 211;
    <I212> = 212;
    <I213> = 213;
    <I214> = 214;
    <I215> = 215;
    <I216> = 216;
    <I217> = 217;
    <I218> = 218;
    <I219> = 219;
    <I220> = 220;
    <I221> = 221;
    <I222> = 222;
    <I223> = 223;
    <I224> = 224;
    <I225> = 225;
    <I226> = 226;
    <I227> = 227;
    <I228> = 228;
    <I229> = 229;
    <I230> = 230;
    <I231> = 231;
    <I232> = 232;
    <I233> = 233;
    <I234> = 234;
    <I235> = 235;
    <I236> = 236;
    <I237> = 237;
    <I238> = 238;
    <I239> = 239;
    <I240> = 240;
    <I241> = 241;
    <I242> = 242;
    <I243> = 243;
    <I244> = 244;
    <I245> = 245;
    <I246> = 246;
    <I247> = 247;
    <I248> = 248;
    <I249> = 249;
    <I250> = 250;
    <I251> = 251;
    <I252> = 252;
    <I253> = 253;
    indicator 1 = "Caps Lock";
    indicator 2 = "Num Lock";
    indicator 3 = "Scroll Lock";
    indicator 4 = "Compose";
    indicator 5 = "Kana";
    indicator 6 = "Sleep";
    indicator 7 = "Suspend";
    indicator 8 = "Mute";
    indicator 9 = "Misc";
    indicator 10 = "Mail";
    indicator 11 = "Charging";
    virtual indicator 12 = "Shift Lock";
    virtual indicator 13 = "Group 2";
    virtual indicator 14 = "Mouse Keys";
    alias <AC12> = <BKSL>;
    alias <MENU> = <COMP>;
    alias <HZTG> = <TLDE>;
    alias <LMTA> = <LWIN>;
    alias <RMTA> = <RWIN>;
    alias <ALGR> = <RALT>;
    alias <KPPT> = <I129>;
    alias <LatQ> = <AD01>;
    alias <LatW> = <AD02>;
    alias <LatE> = <AD03>;
    alias <LatR> = <AD04>;
    alias <LatT> = <AD05>;
    alias <LatY> = <AD06>;
    alias <LatU> = <AD07>;
    alias <LatI> = <AD08>;
    alias <LatO> = <AD09>;
    alias <LatP> = <AD10>;
    alias <LatA> = <AC01>;
    alias <LatS> = <AC02>;
    alias <LatD> = <AC03>;
    alias <LatF> = <AC04>;
    alias <LatG> = <AC05>;
    alias <LatH> = <AC06>;
    alias <LatJ> = <AC07>;
    alias <LatK> = <AC08>;
    alias <LatL> = <AC09>;
    alias <LatZ> = <AB01>;
    alias <LatX> = <AB02>;
    alias <LatC> = <AB03>;
    alias <LatV> = <AB04>;
    alias <LatB> = <AB05>;
    alias <LatN> = <AB06>;
    alias <LatM> = <AB07>;
};

xkb_types "complete" {

    virtual_modifiers NumLock,Alt,LevelThree,LAlt,RAlt,RControl,LControl,ScrollLock,LevelFive,AltGr,Meta,Super,Hyper;

    type "ONE_LEVEL" {
        modifiers= none;
        level_name[Level1]= "Any";
    };
    type "TWO_LEVEL" {
        modifiers= Shift;
        map[Shift]= Level2;
        level_name[Level1]= "Base";
        level_name[Level2]= "Shift";
    };
    type "ALPHABETIC" {
        modifiers= Shift+Lock;
        map[Shift]= Level2;
        map[Lock]= Level2;
        level_name[Level1]= "Base";
        level_name[Level2]= "Caps";
    };
    type "KEYPAD" {
        modifiers= Shift+NumLock;
        map[Shift]= Level2;
        map[NumLock]= Level2;
        level_name[Level1]= "Base";
        level_name[Level2]= "Number";
    };
    type "SHIFT+ALT" {
        modifiers= Shift+Alt;
        map[Shift+Alt]= Level2;
        level_name[Level1]= "Base";
        level_name[Level2]= "Shift+Alt";
    };
    type "PC_SUPER_LEVEL2" {
        modifiers= Mod4;
        map[Mod4]= Level2;
        level_name[Level1]= "Base";
        level_name[Level2]= "Super";
    };
    type "PC_CONTROL_LEVEL2" {
        modifiers= Control;
        map[Control]= Level2;
        level_name[Level1]= "Base";
        level_name[Level2]= "Control";
    };
    type "PC_LCONTROL_LEVEL2" {
        modifiers= LControl;
        map[LControl]= Level2;
        level_name[Level1]= "Base";
        level_name[Level2]= "LControl";
    };
    type "PC_RCONTROL_LEVEL2" {
        modifiers= RControl;
        map[RControl]= Level2;
        level_name[Level1]= "Base";
        level_name[Level2]= "RControl";
    };
    type "PC_ALT_LEVEL2" {
        modifiers= Alt;
        map[Alt]= Level2;
        level_name[Level1]= "Base";
        level_name[Level2]= "Alt";
    };
    type "PC_LALT_LEVEL2" {
        modifiers= LAlt;
        map[LAlt]= Level2;
        level_name[Level1]= "Base";
        level_name[Level2]= "LAlt";
    };
    type "PC_RALT_LEVEL2" {
        modifiers= RAlt;
        map[RAlt]= Level2;
        level_name[Level1]= "Base";
        level_name[Level2]= "RAlt";
    };
    type "CTRL+ALT" {
        modifiers= Shift+Control+Alt+LevelThree;
        map[Shift]= Level2;
        preserve[Shift]= Shift;
        map[LevelThree]= Level3;
        map[Shift+LevelThree]= Level4;
        preserve[Shift+LevelThree]= Shift;
        map[Control+Alt]= Level5;
        level_name[Level1]= "Base";
        level_name[Level2]= "Shift";
        level_name[Level3]= "Alt Base";
        level_name[Level4]= "Shift Alt";
        level_name[Level5]= "Ctrl+Alt";
    };
    type "LOCAL_EIGHT_LEVEL" {
        modifiers= Shift+Lock+Control+LevelThree;
        map[Shift+Lock]= Level1;
        map[Shift]= Level2;
        map[Lock]= Level2;
        map[LevelThree]= Level3;
        map[Shift+Lock+LevelThree]= Level3;
        map[Shift+LevelThree]= Level4;
        map[Lock+LevelThree]= Level4;
        map[Control]= Level5;
        map[Shift+Lock+Control]= Level5;
        map[Shift+Control]= Level6;
        map[Lock+Control]= Level6;
        map[Control+LevelThree]= Level7;
        map[Shift+Lock+Control+LevelThree]= Level7;
        map[Shift+Control+LevelThree]= Level8;
        map[Lock+Control+LevelThree]= Level8;
        level_name[Level1]= "Base";
        level_name[Level2]= "Shift";
        level_name[Level3]= "Level3";
        level_name[Level4]= "Shift Level3";
        level_name[Level5]= "Ctrl";
        level_name[Level6]= "Shift Ctrl";
        level_name[Level7]= "Level3 Ctrl";
        level_name[Level8]= "Shift Level3 Ctrl";
    };
    type "THREE_LEVEL" {
        modifiers= Shift+LevelThree;
        map[Shift]= Level2;
        map[LevelThree]= Level3;
        map[Shift+LevelThree]= Level3;
        level_name[Level1]= "Base";
        level_name[Level2]= "Shift";
        level_name[Level3]= "Level3";
    };
    type "EIGHT_LEVEL" {
        modifiers= Shift+LevelThree+LevelFive;
        map[Shift]= Level2;
        map[LevelThree]= Level3;
        map[Shift+LevelThree]= Level4;
        map[LevelFive]= Level5;
        map[Shift+LevelFive]= Level6;
        map[LevelThree+LevelFive]= Level7;
        map[Shift+LevelThree+LevelFive]= Level8;
        level_name[Level1]= "Base";
        level_name[Level2]= "Shift";
        level_name[Level3]= "Alt Base";
        level_name[Level4]= "Shift Alt";
        level_name[Level5]= "X";
        level_name[Level6]= "X Shift";
        level_name[Level7]= "X Alt Base";
        level_name[Level8]= "X Shift Alt";
    };
    type "EIGHT_LEVEL_ALPHABETIC" {
        modifiers= Shift+Lock+LevelThree+LevelFive;
        map[Shift]= Level2;
        map[Lock]= Level2;
        map[LevelThree]= Level3;
        map[Shift+LevelThree]= Level4;
        map[Lock+LevelThree]= Level4;
        map[Shift+Lock+LevelThree]= Level3;
        map[LevelFive]= Level5;
        map[Shift+LevelFive]= Level6;
        map[Lock+LevelFive]= Level6;
        map[LevelThree+LevelFive]= Level7;
        map[Shift+LevelThree+LevelFive]= Level8;
        map[Lock+LevelThree+LevelFive]= Level8;
        map[Shift+Lock+LevelThree+LevelFive]= Level7;
        level_name[Level1]= "Base";
        level_name[Level2]= "Shift";
        level_name[Level3]= "Alt Base";
        level_name[Level4]= "Shift Alt";
        level_name[Level5]= "X";
        level_name[Level6]= "X Shift";
        level_name[Level7]= "X Alt Base";
        level_name[Level8]= "X Shift Alt";
    };
    type "EIGHT_LEVEL_SEMIALPHABETIC" {
        modifiers= Shift+Lock+LevelThree+LevelFive;
        map[Shift]= Level2;
        map[Lock]= Level2;
        map[LevelThree]= Level3;
        map[Shift+LevelThree]= Level4;
        map[Lock+LevelThree]= Level3;
        preserve[Lock+LevelThree]= Lock;
        map[Shift+Lock+LevelThree]= Level4;
        preserve[Shift+Lock+LevelThree]= Lock;
        map[LevelFive]= Level5;
        map[Shift+LevelFive]= Level6;
        map[Lock+LevelFive]= Level6;
        preserve[Lock+LevelFive]= Lock;
        map[Shift+Lock+LevelFive]= Level6;
        preserve[Shift+Lock+LevelFive]= Lock;
        map[LevelThree+LevelFive]= Level7;
        map[Shift+LevelThree+LevelFive]= Level8;
        map[Lock+LevelThree+LevelFive]= Level7;
        preserve[Lock+LevelThree+LevelFive]= Lock;
        map[Shift+Lock+LevelThree+LevelFive]= Level8;
        preserve[Shift+Lock+LevelThree+LevelFive]= Lock;
        level_name[Level1]= "Base";
        level_name[Level2]= "Shift";
        level_name[Level3]= "Alt Base";
        level_name[Level4]= "Shift Alt";
        level_name[Level5]= "X";
        level_name[Level6]= "X Shift";
        level_name[Level7]= "X Alt Base";
        level_name[Level8]= "X Shift Alt";
    };
    type "FOUR_LEVEL" {
        modifiers= Shift+LevelThree;
        map[Shift]= Level2;
        map[LevelThree]= Level3;
        map[Shift+LevelThree]= Level4;
        level_name[Level1]= "Base";
        level_name[Level2]= "Shift";
        level_name[Level3]= "Alt Base";
        level_name[Level4]= "Shift Alt";
    };
    type "FOUR_LEVEL_ALPHABETIC" {
        modifiers= Shift+Lock+LevelThree;
        map[Shift]= Level2;
        map[Lock]= Level2;
        map[LevelThree]= Level3;
        map[Shift+LevelThree]= Level4;
        map[Lock+LevelThree]= Level4;
        map[Shift+Lock+LevelThree]= Level3;
        level_name[Level1]= "Base";
        level_name[Level2]= "Shift";
        level_name[Level3]= "Alt Base";
        level_name[Level4]= "Shift Alt";
    };
    type "FOUR_LEVEL_SEMIALPHABETIC" {
        modifiers= Shift+Lock+LevelThree;
        map[Shift]= Level2;
        map[Lock]= Level2;
        map[LevelThree]= Level3;
        map[Shift+LevelThree]= Level4;
        map[Lock+LevelThree]= Level3;
        preserve[Lock+LevelThree]= Lock;
        map[Shift+Lock+LevelThree]= Level4;
        preserve[Shift+Lock+LevelThree]= Lock;
        level_name[Level1]= "Base";
        level_name[Level2]= "Shift";
        level_name[Level3]= "Alt Base";
        level_name[Level4]= "Shift Alt";
    };
    type "FOUR_LEVEL_MIXED_KEYPAD" {
        modifiers= Shift+NumLock+LevelThree;
        map[Shift+NumLock]= Level1;
        map[NumLock]= Level2;
        map[Shift]= Level2;
        map[LevelThree]= Level3;
        map[NumLock+LevelThree]= Level3;
        map[Shift+LevelThree]= Level4;
        map[Shift+NumLock+LevelThree]= Level4;
        level_name[Level1]= "Base";
        level_name[Level2]= "Number";
        level_name[Level3]= "Alt Base";
        level_name[Level4]= "Shift Alt";
    };
    type "FOUR_LEVEL_X" {
        modifiers= Shift+Control+Alt+LevelThree;
        map[LevelThree]= Level2;
        map[Shift+LevelThree]= Level3;
        map[Control+Alt]= Level4;
        level_name[Level1]= "Base";
        level_name[Level2]= "Alt Base";
        level_name[Level3]= "Shift Alt";
        level_name[Level4]= "Ctrl+Alt";
    };
    type "SEPARATE_CAPS_AND_SHIFT_ALPHABETIC" {
        modifiers= Shift+Lock+LevelThree;
        map[Shift]= Level2;
        map[Lock]= Level4;
        preserve[Lock]= Lock;
        map[LevelThree]= Level3;
        map[Shift+LevelThree]= Level4;
        map[Lock+LevelThree]= Level3;
        preserve[Lock+LevelThree]= Lock;
        map[Shift+Lock+LevelThree]= Level3;
        level_name[Level1]= "Base";
        level_name[Level2]= "Shift";
        level_name[Level3]= "AltGr Base";
        level_name[Level4]= "Shift AltGr";
    };
    type "FOUR_LEVEL_PLUS_LOCK" {
        modifiers= Shift+Lock+LevelThree;
        map[Shift]= Level2;
        map[LevelThree]= Level3;
        map[Shift+LevelThree]= Level4;
        map[Lock]= Level5;
        map[Shift+Lock]= Level2;
        map[Lock+LevelThree]= Level3;
        map[Shift+Lock+LevelThree]= Level4;
        level_name[Level1]= "Base";
        level_name[Level2]= "Shift";
        level_name[Level3]= "Alt Base";
        level_name[Level4]= "Shift Alt";
        level_name[Level5]= "Lock";
    };
    type "FOUR_LEVEL_KEYPAD" {
        modifiers= Shift+NumLock+LevelThree;
        map[Shift]= Level2;
        map[NumLock]= Level2;
        map[LevelThree]= Level3;
        map[Shift+LevelThree]= Level4;
        map[NumLock+LevelThree]= Level4;
        map[Shift+NumLock+LevelThree]= Level3;
        level_name[Level1]= "Base";
        level_name[Level2]= "Number";
        level_name[Level3]= "Alt Base";
        level_name[Level4]= "Alt Number";
    };
};

xkb_compatibility "complete" {

    virtual_modifiers NumLock,Alt,LevelThree,LAlt,RAlt,RControl,LControl,ScrollLock,LevelFive,AltGr,Meta,Super,Hyper;

    interpret.useModMapMods= AnyLevel;
    interpret.repeat= False;
    interpret.locking= False;
    interpret ISO_Level2_Latch+Exactly(Shift) {
        useModMapMods=level1;
        action= LatchMods(modifiers=Shift,clearLocks,latchToLock);
    };
    interpret Shift_Lock+AnyOf(Shift+Lock) {
        action= LockMods(modifiers=Shift);
    };
    interpret Num_Lock+AnyOf(all) {
        virtualModifier= NumLock;
        action= LockMods(modifiers=NumLock);
    };
    interpret ISO_Level3_Shift+AnyOf(all) {
        virtualModifier= LevelThree;
        useModMapMods=level1;
        action= SetMods(modifiers=LevelThree,clearLocks);
    };
    interpret ISO_Level3_Latch+AnyOf(all) {
        virtualModifier= LevelThree;
        useModMapMods=level1;
        action= LatchMods(modifiers=LevelThree,clearLocks,latchToLock);
    };
    interpret ISO_Level3_Lock+AnyOf(all) {
        virtualModifier= LevelThree;
        useModMapMods=level1;
        action= LockMods(modifiers=LevelThree);
    };
    interpret Alt_L+AnyOf(all) {
        virtualModifier= Alt;
        action= SetMods(modifiers=modMapMods,clearLocks);
    };
    interpret Alt_R+AnyOf(all) {
        virtualModifier= Alt;
        action= SetMods(modifiers=modMapMods,clearLocks);
    };
    interpret Meta_L+AnyOf(all) {
        virtualModifier= Meta;
        action= SetMods(modifiers=modMapMods,clearLocks);
    };
    interpret Meta_R+AnyOf(all) {
        virtualModifier= Meta;
        action= SetMods(modifiers=modMapMods,clearLocks);
    };
    interpret Super_L+AnyOf(all) {
        virtualModifier= Super;
        action= SetMods(modifiers=modMapMods,clearLocks);
    };
    interpret Super_R+AnyOf(all) {
        virtualModifier= Super;
        action= SetMods(modifiers=modMapMods,clearLocks);
    };
    interpret Hyper_L+AnyOf(all) {
        virtualModifier= Hyper;
        action= SetMods(modifiers=modMapMods,clearLocks);
    };
    interpret Hyper_R+AnyOf(all) {
        virtualModifier= Hyper;
        action= SetMods(modifiers=modMapMods,clearLocks);
    };
    interpret Scroll_Lock+AnyOf(all) {
        virtualModifier= ScrollLock;
        action= LockMods(modifiers=modMapMods);
    };
    interpret ISO_Level5_Shift+AnyOf(all) {
        virtualModifier= LevelFive;
        useModMapMods=level1;
        action= SetMods(modifiers=LevelFive,clearLocks);
    };
    interpret ISO_Level5_Latch+AnyOf(all) {
        virtualModifier= LevelFive;
        useModMapMods=level1;
        action= LatchMods(modifiers=LevelFive,clearLocks,latchToLock);
    };
    interpret ISO_Level5_Lock+AnyOf(all) {
        virtualModifier= LevelFive;
        useModMapMods=level1;
        action= LockMods(modifiers=LevelFive);
    };
    interpret Mode_switch+AnyOfOrNone(all) {
        virtualModifier= AltGr;
        useModMapMods=level1;
        action= SetGroup(group=+1);
    };
    interpret ISO_Level3_Shift+AnyOfOrNone(all) {
        action= SetMods(modifiers=LevelThree,clearLocks);
    };
    interpret ISO_Level3_Latch+AnyOfOrNone(all) {
        action= LatchMods(modifiers=LevelThree,clearLocks,latchToLock);
    };
    interpret ISO_Level3_Lock+AnyOfOrNone(all) {
        action= LockMods(modifiers=LevelThree);
    };
    interpret ISO_Group_Latch+AnyOfOrNone(all) {
        virtualModifier= AltGr;
        useModMapMods=level1;
        action= LatchGroup(group=2);
    };
    interpret ISO_Next_Group+AnyOfOrNone(all) {
        virtualModifier= AltGr;
        useModMapMods=level1;
        action= LockGroup(group=+1);
    };
    interpret ISO_Prev_Group+AnyOfOrNone(all) {
        virtualModifier= AltGr;
        useModMapMods=level1;
        action= LockGroup(group=-1);
    };
    interpret ISO_First_Group+AnyOfOrNone(all) {
        action= LockGroup(group=1);
    };
    interpret ISO_Last_Group+AnyOfOrNone(all) {
        action= LockGroup(group=2);
    };
    interpret KP_1+AnyOfOrNone(all) {
        repeat= True;
        action= MovePtr(x=-1,y=+1);
    };
    interpret KP_End+AnyOfOrNone(all) {
        repeat= True;
        action= MovePtr(x=-1,y=+1);
    };
    interpret KP_2+AnyOfOrNone(all) {
        repeat= True;
        action= MovePtr(x=+0,y=+1);
    };
    interpret KP_Down+AnyOfOrNone(all) {
        repeat= True;
        action= MovePtr(x=+0,y=+1);
    };
    interpret KP_3+AnyOfOrNone(all) {
        repeat= True;
        action= MovePtr(x=+1,y=+1);
    };
    interpret KP_Next+AnyOfOrNone(all) {
        repeat= True;
        action= MovePtr(x=+1,y=+1);
    };
    interpret KP_4+AnyOfOrNone(all) {
        repeat= True;
        action= MovePtr(x=-1,y=+0);
    };
    interpret KP_Left+AnyOfOrNone(all) {
        repeat= True;
        action= MovePtr(x=-1,y=+0);
    };
    interpret KP_6+AnyOfOrNone(all) {
        repeat= True;
        action= MovePtr(x=+1,y=+0);
    };
    interpret KP_Right+AnyOfOrNone(all) {
        repeat= True;
        action= MovePtr(x=+1,y=+0);
    };
    interpret KP_7+AnyOfOrNone(all) {
        repeat= True;
        action= MovePtr(x=-1,y=-1);
    };
    interpret KP_Home+AnyOfOrNone(all) {
        repeat= True;
        action= MovePtr(x=-1,y=-1);
    };
    interpret KP_8+AnyOfOrNone(all) {
        repeat= True;
        action= MovePtr(x=+0,y=-1);
    };
    interpret KP_Up+AnyOfOrNone(all) {
        repeat= True;
        action= MovePtr(x=+0,y=-1);
    };
    interpret KP_9+AnyOfOrNone(all) {
        repeat= True;
        action= MovePtr(x=+1,y=-1);
    };
    interpret KP_Prior+AnyOfOrNone(all) {
        repeat= True;
        action= MovePtr(x=+1,y=-1);
    };
    interpret KP_5+AnyOfOrNone(all) {
        repeat= True;
        action= PtrBtn(button=default);
    };
    interpret KP_Begin+AnyOfOrNone(all) {
        repeat= True;
        action= PtrBtn(button=default);
    };
    interpret KP_F2+AnyOfOrNone(all) {
        repeat= True;
        action= SetPtrDflt(affect=button,button=1);
    };
    interpret KP_Divide+AnyOfOrNone(all) {
        repeat= True;
        action= SetPtrDflt(affect=button,button=1);
    };
    interpret KP_F3+AnyOfOrNone(all) {
        repeat= True;
        action= SetPtrDflt(affect=button,button=2);
    };
    interpret KP_Multiply+AnyOfOrNone(all) {
        repeat= True;
        action= SetPtrDflt(affect=button,button=2);
    };
    interpret KP_F4+AnyOfOrNone(all) {
        repeat= True;
        action= SetPtrDflt(affect=button,button=3);
    };
    interpret KP_Subtract+AnyOfOrNone(all) {
        repeat= True;
        action= SetPtrDflt(affect=button,button=3);
    };
    interpret KP_Separator+AnyOfOrNone(all) {
        repeat= True;
        action= PtrBtn(button=default,count=2);
    };
    interpret KP_Add+AnyOfOrNone(all) {
        repeat= True;
        action= PtrBtn(button=default,count=2);
    };
    interpret KP_0+AnyOfOrNone(all) {
        repeat= True;
        action= LockPtrBtn(button=default,affect=lock);
    };
    interpret KP_Insert+AnyOfOrNone(all) {
        repeat= True;
        action= LockPtrBtn(button=default,affect=lock);
    };
    interpret KP_Decimal+AnyOfOrNone(all) {
        repeat= True;
        action= LockPtrBtn(button=default,affect=unlock);
    };
    interpret KP_Delete+AnyOfOrNone(all) {
        repeat= True;
        action= LockPtrBtn(button=default,affect=unlock);
    };
    interpret F25+AnyOfOrNone(all) {
        repeat= True;
        action= SetPtrDflt(affect=button,button=1);
    };
    interpret F26+AnyOfOrNone(all) {
        repeat= True;
        action= SetPtrDflt(affect=button,button=2);
    };
    interpret F27+AnyOfOrNone(all) {
        repeat= True;
        action= MovePtr(x=-1,y=-1);
    };
    interpret F29+AnyOfOrNone(all) {
        repeat= True;
        action= MovePtr(x=+1,y=-1);
    };
    interpret F31+AnyOfOrNone(all) {
        repeat= True;
        action= PtrBtn(button=default);
    };
    interpret F33+AnyOfOrNone(all) {
        repeat= True;
        action= MovePtr(x=-1,y=+1);
    };
    interpret F35+AnyOfOrNone(all) {
        repeat= True;
        action= MovePtr(x=+1,y=+1);
    };
    interpret Pointer_Button_Dflt+AnyOfOrNone(all) {
        action= PtrBtn(button=default);
    };
    interpret Pointer_Button1+AnyOfOrNone(all) {
        action= PtrBtn(button=1);
    };
    interpret Pointer_Button2+AnyOfOrNone(all) {
        action= PtrBtn(button=2);
    };
    interpret Pointer_Button3+AnyOfOrNone(all) {
        action= PtrBtn(button=3);
    };
    interpret Pointer_DblClick_Dflt+AnyOfOrNone(all) {
        action= PtrBtn(button=default,count=2);
    };
    interpret Pointer_DblClick1+AnyOfOrNone(all) {
        action= PtrBtn(button=1,count=2);
    };
    interpret Pointer_DblClick2+AnyOfOrNone(all) {
        action= PtrBtn(button=2,count=2);
    };
    interpret Pointer_DblClick3+AnyOfOrNone(all) {
        action= PtrBtn(button=3,count=2);
    };
    interpret Pointer_Drag_Dflt+AnyOfOrNone(all) {
        action= LockPtrBtn(button=default,affect=both);
    };
    interpret Pointer_Drag1+AnyOfOrNone(all) {
        action= LockPtrBtn(button=1,affect=both);
    };
    interpret Pointer_Drag2+AnyOfOrNone(all) {
        action= LockPtrBtn(button=2,affect=both);
    };
    interpret Pointer_Drag3+AnyOfOrNone(all) {
        action= LockPtrBtn(button=3,affect=both);
    };
    interpret Pointer_EnableKeys+AnyOfOrNone(all) {
        action= LockControls(controls=MouseKeys);
    };
    interpret Pointer_Accelerate+AnyOfOrNone(all) {
        action= LockControls(controls=MouseKeysAccel);
    };
    interpret Pointer_DfltBtnNext+AnyOfOrNone(all) {
        action= SetPtrDflt(affect=button,button=+1);
    };
    interpret Pointer_DfltBtnPrev+AnyOfOrNone(all) {
        action= SetPtrDflt(affect=button,button=-1);
    };
    interpret AccessX_Enable+AnyOfOrNone(all) {
        action= LockControls(controls=AccessXKeys);
    };
    interpret AccessX_Feedback_Enable+AnyOfOrNone(all) {
        action= LockControls(controls=AccessXFeedback);
    };
    interpret RepeatKeys_Enable+AnyOfOrNone(all) {
        action= LockControls(controls=RepeatKeys);
    };
    interpret SlowKeys_Enable+AnyOfOrNone(all) {
        action= LockControls(controls=SlowKeys);
    };
    interpret BounceKeys_Enable+AnyOfOrNone(all) {
        action= LockControls(controls=BounceKeys);
    };
    interpret StickyKeys_Enable+AnyOfOrNone(all) {
        action= LockControls(controls=StickyKeys);
    };
    interpret MouseKeys_Enable+AnyOfOrNone(all) {
        action= LockControls(controls=MouseKeys);
    };
    interpret MouseKeys_Accel_Enable+AnyOfOrNone(all) {
        action= LockControls(controls=MouseKeysAccel);
    };
    interpret Overlay1_Enable+AnyOfOrNone(all) {
        action= LockControls(controls=Overlay1);
    };
    interpret Overlay2_Enable+AnyOfOrNone(all) {
        action= LockControls(controls=Overlay2);
    };
    interpret AudibleBell_Enable+AnyOfOrNone(all) {
        action= LockControls(controls=AudibleBell);
    };
    interpret Terminate_Server+AnyOfOrNone(all) {
        action= Terminate();
    };
    interpret Alt_L+AnyOfOrNone(all) {
        action= SetMods(modifiers=Alt,clearLocks);
    };
    interpret Alt_R+AnyOfOrNone(all) {
        action= SetMods(modifiers=Alt,clearLocks);
    };
    interpret Meta_L+AnyOfOrNone(all) {
        action= SetMods(modifiers=Meta,clearLocks);
    };
    interpret Meta_R+AnyOfOrNone(all) {
        action= SetMods(modifiers=Meta,clearLocks);
    };
    interpret Super_L+AnyOfOrNone(all) {
        action= SetMods(modifiers=Super,clearLocks);
    };
    interpret Super_R+AnyOfOrNone(all) {
        action= SetMods(modifiers=Super,clearLocks);
    };
    interpret Hyper_L+AnyOfOrNone(all) {
        action= SetMods(modifiers=Hyper,clearLocks);
    };
    interpret Hyper_R+AnyOfOrNone(all) {
        action= SetMods(modifiers=Hyper,clearLocks);
    };
    interpret Shift_L+AnyOfOrNone(all) {
        action= SetMods(modifiers=Shift,clearLocks);
    };
    interpret XF86Switch_VT_1+AnyOfOrNone(all) {
        repeat= True;
        action= SwitchScreen(screen=1,!same);
    };
    interpret XF86Switch_VT_2+AnyOfOrNone(all) {
        repeat= True;
        action= SwitchScreen(screen=2,!same);
    };
    interpret XF86Switch_VT_3+AnyOfOrNone(all) {
        repeat= True;
        action= SwitchScreen(screen=3,!same);
    };
    interpret XF86Switch_VT_4+AnyOfOrNone(all) {
        repeat= True;
        action= SwitchScreen(screen=4,!same);
    };
    interpret XF86Switch_VT_5+AnyOfOrNone(all) {
        repeat= True;
        action= SwitchScreen(screen=5,!same);
    };
    interpret XF86Switch_VT_6+AnyOfOrNone(all) {
        repeat= True;
        action= SwitchScreen(screen=6,!same);
    };
    interpret XF86Switch_VT_7+AnyOfOrNone(all) {
        repeat= True;
        action= SwitchScreen(screen=7,!same);
    };
    interpret XF86Switch_VT_8+AnyOfOrNone(all) {
        repeat= True;
        action= SwitchScreen(screen=8,!same);
    };
    interpret XF86Switch_VT_9+AnyOfOrNone(all) {
        repeat= True;
        action= SwitchScreen(screen=9,!same);
    };
    interpret XF86Switch_VT_10+AnyOfOrNone(all) {
        repeat= True;
        action= SwitchScreen(screen=10,!same);
    };
    interpret XF86Switch_VT_11+AnyOfOrNone(all) {
        repeat= True;
        action= SwitchScreen(screen=11,!same);
    };
    interpret XF86Switch_VT_12+AnyOfOrNone(all) {
        repeat= True;
        action= SwitchScreen(screen=12,!same);
    };
    interpret XF86LogGrabInfo+AnyOfOrNone(all) {
        repeat= True;
        action= Private(type=0x86,data[0]=0x50,data[1]=0x72,data[2]=0x47,data[3]=0x72,data[4]=0x62,data[5]=0x73,data[6]=0x00);
    };
    interpret XF86LogWindowTree+AnyOfOrNone(all) {
        repeat= True;
        action= Private(type=0x86,data[0]=0x50,data[1]=0x72,data[2]=0x57,data[3]=0x69,data[4]=0x6e,data[5]=0x73,data[6]=0x00);
    };
    interpret XF86Next_VMode+AnyOfOrNone(all) {
        repeat= True;
        action= Private(type=0x86,data[0]=0x2b,data[1]=0x56,data[2]=0x4d,data[3]=0x6f,data[4]=0x64,data[5]=0x65,data[6]=0x00);
    };
    interpret XF86Prev_VMode+AnyOfOrNone(all) {
        repeat= True;
        action= Private(type=0x86,data[0]=0x2d,data[1]=0x56,data[2]=0x4d,data[3]=0x6f,data[4]=0x64,data[5]=0x65,data[6]=0x00);
    };
    interpret ISO_Level5_Shift+AnyOfOrNone(all) {
        action= SetMods(modifiers=LevelFive,clearLocks);
    };
    interpret ISO_Level5_Latch+AnyOfOrNone(all) {
        action= LatchMods(modifiers=LevelFive,clearLocks,latchToLock);
    };
    interpret ISO_Level5_Lock+AnyOfOrNone(all) {
        action= LockMods(modifiers=LevelFive);
    };
    interpret Caps_Lock+AnyOfOrNone(all) {
        action= LockMods(modifiers=Lock);
    };
    interpret Any+Exactly(Lock) {
        action= LockMods(modifiers=Lock);
    };
    interpret Any+AnyOf(all) {
        action= SetMods(modifiers=modMapMods,clearLocks);
    };
    group 2 = AltGr;
    group 3 = AltGr;
    group 4 = AltGr;
    indicator "Caps Lock" {
        !allowExplicit;
        whichModState= locked;
        modifiers= Lock;
    };
    indicator "Num Lock" {
        !allowExplicit;
        whichModState= locked;
        modifiers= NumLock;
    };
    indicator "Scroll Lock" {
        whichModState= locked;
        modifiers= ScrollLock;
    };
    indicator "Shift Lock" {
        !allowExplicit;
        whichModState= locked;
        modifiers= Shift;
    };
    indicator "Group 2" {
        !allowExplicit;
        groups= 0xfe;
    };
    indicator "Mouse Keys" {
        indicatorDrivesKeyboard;
        controls= mouseKeys;
    };
};

xkb_symbols "pc+gb+us:2+inet(evdev)+compose(ralt)" {

    name[group1]="English (UK)";
    name[group2]="English (US)";

    key  <ESC> {         [          Escape ] };
    key <AE01> {
        type[group1]= "FOUR_LEVEL",
        symbols[Group1]= [               1,          exclam,     onesuperior,      exclamdown ],
        symbols[Group2]= [               1,          exclam ]
    };
    key <AE02> {
        type[group1]= "FOUR_LEVEL",
        symbols[Group1]= [               2,        quotedbl,     twosuperior,       oneeighth ],
        symbols[Group2]= [               2,              at ]
    };
    key <AE03> {
        type[group1]= "FOUR_LEVEL",
        symbols[Group1]= [               3,        sterling,   threesuperior,        sterling ],
        symbols[Group2]= [               3,      numbersign ]
    };
    key <AE04> {
        type[group1]= "FOUR_LEVEL",
        symbols[Group1]= [               4,          dollar,        EuroSign,      onequarter ],
        symbols[Group2]= [               4,          dollar ]
    };
    key <AE05> {
        type[group1]= "FOUR_LEVEL",
        symbols[Group1]= [               5,         percent,         onehalf,    threeeighths ],
        symbols[Group2]= [               5,         percent ]
    };
    key <AE06> {
        type[group1]= "FOUR_LEVEL",
        symbols[Group1]= [               6,     asciicircum,   threequarters,     fiveeighths ],
        symbols[Group2]= [               6,     asciicircum ]
    };
    key <AE07> {
        type[group1]= "FOUR_LEVEL",
        symbols[Group1]= [               7,       ampersand,       braceleft,    seveneighths ],
        symbols[Group2]= [               7,       ampersand ]
    };
    key <AE08> {
        type[group1]= "FOUR_LEVEL",
        symbols[Group1]= [               8,        asterisk,     bracketleft,       trademark ],
        symbols[Group2]= [               8,        asterisk ]
    };
    key <AE09> {
        type[group1]= "FOUR_LEVEL",
        symbols[Group1]= [               9,       parenleft,    bracketright,       plusminus ],
        symbols[Group2]= [               9,       parenleft ]
    };
    key <AE10> {
        type[group1]= "FOUR_LEVEL",
        symbols[Group1]= [               0,      parenright,      braceright,          degree ],
        symbols[Group2]= [               0,      parenright ]
    };
    key <AE11> {
        type[group1]= "FOUR_LEVEL",
        symbols[Group1]= [           minus,      underscore,       backslash,    questiondown ],
        symbols[Group2]= [           minus,      underscore ]
    };
    key <AE12> {
        type[group1]= "FOUR_LEVEL",
        symbols[Group1]= [           equal,            plus,    dead_cedilla,     dead_ogonek ],
        symbols[Group2]= [           equal,            plus ]
    };
    key <BKSP> {         [       BackSpace,       BackSpace ] };
    key  <TAB> {         [             Tab,    ISO_Left_Tab ] };
    key <AD01> {
        type[group1]= "FOUR_LEVEL_SEMIALPHABETIC",
        type[group2]= "ALPHABETIC",
        symbols[Group1]= [               q,               Q,              at,     Greek_OMEGA ],
        symbols[Group2]= [               q,               Q ]
    };
    key <AD02> {
        type[group1]= "FOUR_LEVEL_ALPHABETIC",
        type[group2]= "ALPHABETIC",
        symbols[Group1]= [               w,               W,         lstroke,         Lstroke ],
        symbols[Group2]= [               w,               W ]
    };
    key <AD03> {
        type[group1]= "FOUR_LEVEL_ALPHABETIC",
        type[group2]= "ALPHABETIC",
        symbols[Group1]= [               e,               E,               e,               E ],
        symbols[Group2]= [               e,               E ]
    };
    key <AD04> {
        type[group1]= "FOUR_LEVEL_SEMIALPHABETIC",
        type[group2]= "ALPHABETIC",
        symbols[Group1]= [               r,               R,       paragraph,      registered ],
        symbols[Group2]= [               r,               R ]
    };
    key <AD05> {
        type[group1]= "FOUR_LEVEL_ALPHABETIC",
        type[group2]= "ALPHABETIC",
        symbols[Group1]= [               t,               T,          tslash,          Tslash ],
        symbols[Group2]= [               t,               T ]
    };
    key <AD06> {
        type[group1]= "FOUR_LEVEL_SEMIALPHABETIC",
        type[group2]= "ALPHABETIC",
        symbols[Group1]= [               y,               Y,       leftarrow,             yen ],
        symbols[Group2]= [               y,               Y ]
    };
    key <AD07> {
        type[group1]= "FOUR_LEVEL_SEMIALPHABETIC",
        type[group2]= "ALPHABETIC",
        symbols[Group1]= [               u,               U,       downarrow,         uparrow ],
        symbols[Group2]= [               u,               U ]
    };
    key <AD08> {
        type[group1]= "FOUR_LEVEL_SEMIALPHABETIC",
        type[group2]= "ALPHABETIC",
        symbols[Group1]= [               i,               I,      rightarrow,        idotless ],
        symbols[Group2]= [               i,               I ]
    };
    key <AD09> {
        type[group1]= "FOUR_LEVEL_ALPHABETIC",
        type[group2]= "ALPHABETIC",
        symbols[Group1]= [               o,               O,          oslash,          Oslash ],
        symbols[Group2]= [               o,               O ]
    };
    key <AD10> {
        type[group1]= "FOUR_LEVEL_ALPHABETIC",
        type[group2]= "ALPHABETIC",
        symbols[Group1]= [               p,               P,           thorn,           THORN ],
        symbols[Group2]= [               p,               P ]
    };
    key <AD11> {
        type[group1]= "FOUR_LEVEL",
        symbols[Group1]= [     bracketleft,       braceleft,  dead_diaeresis,  dead_abovering ],
        symbols[Group2]= [     bracketleft,       braceleft ]
    };
    key <AD12> {
        type[group1]= "FOUR_LEVEL",
        symbols[Group1]= [    bracketright,      braceright,      dead_tilde,     dead_macron ],
        symbols[Group2]= [    bracketright,      braceright ]
    };
    key <RTRN> {         [          Return ] };
    key <LCTL> {         [       Control_L ] };
    key <AC01> {
        type[group1]= "FOUR_LEVEL_ALPHABETIC",
        type[group2]= "ALPHABETIC",
        symbols[Group1]= [               a,               A,              ae,              AE ],
        symbols[Group2]= [               a,               A ]
    };
    key <AC02> {
        type[group1]= "FOUR_LEVEL_SEMIALPHABETIC",
        type[group2]= "ALPHABETIC",
        symbols[Group1]= [               s,               S,          ssharp,         section ],
        symbols[Group2]= [               s,               S ]
    };
    key <AC03> {
        type[group1]= "FOUR_LEVEL_ALPHABETIC",
        type[group2]= "ALPHABETIC",
        symbols[Group1]= [               d,               D,             eth,             ETH ],
        symbols[Group2]= [               d,               D ]
    };
    key <AC04> {
        type[group1]= "FOUR_LEVEL_SEMIALPHABETIC",
        type[group2]= "ALPHABETIC",
        symbols[Group1]= [               f,               F,         dstroke,     ordfeminine ],
        symbols[Group2]= [               f,               F ]
    };
    key <AC05> {
        type[group1]= "FOUR_LEVEL_ALPHABETIC",
        type[group2]= "ALPHABETIC",
        symbols[Group1]= [               g,               G,             eng,             ENG ],
        symbols[Group2]= [               g,               G ]
    };
    key <AC06> {
        type[group1]= "FOUR_LEVEL_ALPHABETIC",
        type[group2]= "ALPHABETIC",
        symbols[Group1]= [               h,               H,         hstroke,         Hstroke ],
        symbols[Group2]= [               h,               H ]
    };
    key <AC07> {
        type[group1]= "FOUR_LEVEL_SEMIALPHABETIC",
        type[group2]= "ALPHABETIC",
        symbols[Group1]= [               j,               J,       dead_hook,       dead_horn ],
        symbols[Group2]= [               j,               J ]
    };
    key <AC08> {
        type[group1]= "FOUR_LEVEL_SEMIALPHABETIC",
        type[group2]= "ALPHABETIC",
        symbols[Group1]= [               k,               K,             kra,       ampersand ],
        symbols[Group2]= [               k,               K ]
    };
    key <AC09> {
        type[group1]= "FOUR_LEVEL_ALPHABETIC",
        type[group2]= "ALPHABETIC",
        symbols[Group1]= [               l,               L,         lstroke,         Lstroke ],
        symbols[Group2]= [               l,               L ]
    };
    key <AC10> {
        type[group1]= "FOUR_LEVEL",
        symbols[Group1]= [       semicolon,           colon,      dead_acute, dead_doubleacute ],
        symbols[Group2]= [       semicolon,           colon ]
    };
    key <AC11> {
        type[group1]= "FOUR_LEVEL",
        symbols[Group1]= [      apostrophe,              at, dead_circumflex,      dead_caron ],
        symbols[Group2]= [      apostrophe,        quotedbl ]
    };
    key <TLDE> {
        type[group1]= "FOUR_LEVEL",
        symbols[Group1]= [           grave,         notsign,             bar,             bar ],
        symbols[Group2]= [           grave,      asciitilde ]
    };
    key <LFSH> {         [         Shift_L ] };
    key <BKSL> {
        type[group1]= "FOUR_LEVEL",
        symbols[Group1]= [      numbersign,      asciitilde,      dead_grave,      dead_breve ],
        symbols[Group2]= [       backslash,             bar ]
    };
    key <AB01> {
        type[group1]= "FOUR_LEVEL_SEMIALPHABETIC",
        type[group2]= "ALPHABETIC",
        symbols[Group1]= [               z,               Z,   guillemotleft,            less ],
        symbols[Group2]= [               z,               Z ]
    };
    key <AB02> {
        type[group1]= "FOUR_LEVEL_SEMIALPHABETIC",
        type[group2]= "ALPHABETIC",
        symbols[Group1]= [               x,               X,  guillemotright,         greater ],
        symbols[Group2]= [               x,               X ]
    };
    key <AB03> {
        type[group1]= "FOUR_LEVEL_SEMIALPHABETIC",
        type[group2]= "ALPHABETIC",
        symbols[Group1]= [               c,               C,            cent,       copyright ],
        symbols[Group2]= [               c,               C ]
    };
    key <AB04> {
        type[group1]= "FOUR_LEVEL_SEMIALPHABETIC",
        type[group2]= "ALPHABETIC",
        symbols[Group1]= [               v,               V, leftdoublequotemark, leftsinglequotemark ],
        symbols[Group2]= [               v,               V ]
    };
    key <AB05> {
        type[group1]= "FOUR_LEVEL_SEMIALPHABETIC",
        type[group2]= "ALPHABETIC",
        symbols[Group1]= [               b,               B, rightdoublequotemark, rightsinglequotemark ],
        symbols[Group2]= [               b,               B ]
    };
    key <AB06> {
        type[group1]= "FOUR_LEVEL_ALPHABETIC",
        type[group2]= "ALPHABETIC",
        symbols[Group1]= [               n,               N,               n,               N ],
        symbols[Group2]= [               n,               N ]
    };
    key <AB07> {
        type[group1]= "FOUR_LEVEL_SEMIALPHABETIC",
        type[group2]= "ALPHABETIC",
        symbols[Group1]= [               m,               M,              mu,       masculine ],
        symbols[Group2]= [               m,               M ]
    };
    key <AB08> {
        type[group1]= "FOUR_LEVEL",
        symbols[Group1]= [           comma,            less,  horizconnector,        multiply ],
        symbols[Group2]= [           comma,            less ]
    };
    key <AB09> {
        type[group1]= "FOUR_LEVEL",
        symbols[Group1]= [          period,         greater,  periodcentered,        division ],
        symbols[Group2]= [          period,         greater ]
    };
    key <AB10> {
        type[group1]= "FOUR_LEVEL",
        symbols[Group1]= [           slash,        question,   dead_belowdot,   dead_abovedot ],
        symbols[Group2]= [           slash,        question ]
    };
    key <RTSH> {         [         Shift_R ] };
    key <KPMU> {
        type= "CTRL+ALT",
        symbols[Group1]= [     KP_Multiply,     KP_Multiply,     KP_Multiply,     KP_Multiply,   XF86ClearGrab ]
    };
    key <LALT> {         [           Alt_L,          Meta_L ] };
    key <SPCE> {         [           space ] };
    key <CAPS> {         [       Caps_Lock ] };
    key <FK01> {
        type= "CTRL+ALT",
        symbols[Group1]= [              F1,              F1,              F1,              F1, XF86Switch_VT_1 ]
    };
    key <FK02> {
        type= "CTRL+ALT",
        symbols[Group1]= [              F2,              F2,              F2,              F2, XF86Switch_VT_2 ]
    };
    key <FK03> {
        type= "CTRL+ALT",
        symbols[Group1]= [              F3,              F3,              F3,              F3, XF86Switch_VT_3 ]
    };
    key <FK04> {
        type= "CTRL+ALT",
        symbols[Group1]= [              F4,              F4,              F4,              F4, XF86Switch_VT_4 ]
    };
    key <FK05> {
        type= "CTRL+ALT",
        symbols[Group1]= [              F5,              F5,              F5,              F5, XF86Switch_VT_5 ]
    };
    key <FK06> {
        type= "CTRL+ALT",
        symbols[Group1]= [              F6,              F6,              F6,              F6, XF86Switch_VT_6 ]
    };
    key <FK07> {
        type= "CTRL+ALT",
        symbols[Group1]= [              F7,              F7,              F7,              F7, XF86Switch_VT_7 ]
    };
    key <FK08> {
        type= "CTRL+ALT",
        symbols[Group1]= [              F8,              F8,              F8,              F8, XF86Switch_VT_8 ]
    };
    key <FK09> {
        type= "CTRL+ALT",
        symbols[Group1]= [              F9,              F9,              F9,              F9, XF86Switch_VT_9 ]
    };
    key <FK10> {
        type= "CTRL+ALT",
        symbols[Group1]= [             F10,             F10,             F10,             F10, XF86Switch_VT_10 ]
    };
    key <NMLK> {         [        Num_Lock ] };
    key <SCLK> {         [     Scroll_Lock ] };
    key  <KP7> {         [         KP_Home,            KP_7 ] };
    key  <KP8> {         [           KP_Up,            KP_8 ] };
    key  <KP9> {         [        KP_Prior,            KP_9 ] };
    key <KPSU> {
        type= "CTRL+ALT",
        symbols[Group1]= [     KP_Subtract,     KP_Subtract,     KP_Subtract,     KP_Subtract,  XF86Prev_VMode ]
    };
    key  <KP4> {         [         KP_Left,            KP_4 ] };
    key  <KP5> {         [        KP_Begin,            KP_5 ] };
    key  <KP6> {         [        KP_Right,            KP_6 ] };
    key <KPAD> {
        type= "CTRL+ALT",
        symbols[Group1]= [          KP_Add,          KP_Add,          KP_Add,          KP_Add,  XF86Next_VMode ]
    };
    key  <KP1> {         [          KP_End,            KP_1 ] };
    key  <KP2> {         [         KP_Down,            KP_2 ] };
    key  <KP3> {         [         KP_Next,            KP_3 ] };
    key  <KP0> {         [       KP_Insert,            KP_0 ] };
    key <KPDL> {         [       KP_Delete,      KP_Decimal ] };
    key <LVL3> {
        type= "ONE_LEVEL",
        symbols[Group1]= [ ISO_Level3_Shift ]
    };
    key <LSGT> {
        type= "FOUR_LEVEL",
        symbols[Group1]= [       backslash,             bar,             bar,       brokenbar ]
    };
    key <FK11> {
        type= "CTRL+ALT",
        symbols[Group1]= [             F11,             F11,             F11,             F11, XF86Switch_VT_11 ]
    };
    key <FK12> {
        type= "CTRL+ALT",
        symbols[Group1]= [             F12,             F12,             F12,             F12, XF86Switch_VT_12 ]
    };
    key <KATA> {         [        Katakana ] };
    key <HIRA> {         [        Hiragana ] };
    key <HENK> {         [     Henkan_Mode ] };
    key <HKTG> {         [ Hiragana_Katakana ] };
    key <MUHE> {         [        Muhenkan ] };
    key <KPEN> {         [        KP_Enter ] };
    key <RCTL> {         [       Control_R ] };
    key <KPDV> {
        type= "CTRL+ALT",
        symbols[Group1]= [       KP_Divide,       KP_Divide,       KP_Divide,       KP_Divide,      XF86Ungrab ]
    };
    key <PRSC> {
        type= "PC_ALT_LEVEL2",
        symbols[Group1]= [           Print,         Sys_Req ]
    };
    key <RALT> {
        type= "TWO_LEVEL",
        symbols[Group1]= [       Multi_key,       Multi_key ]
    };
    key <LNFD> {         [        Linefeed ] };
    key <HOME> {         [            Home ] };
    key   <UP> {         [              Up ] };
    key <PGUP> {         [           Prior ] };
    key <LEFT> {         [            Left ] };
    key <RGHT> {         [           Right ] };
    key  <END> {         [             End ] };
    key <DOWN> {         [            Down ] };
    key <PGDN> {         [            Next ] };
    key  <INS> {         [          Insert ] };
    key <DELE> {         [          Delete ] };
    key <MUTE> {         [   XF86AudioMute ] };
    key <VOL-> {         [ XF86AudioLowerVolume ] };
    key <VOL+> {         [ XF86AudioRaiseVolume ] };
    key <POWR> {         [    XF86PowerOff ] };
    key <KPEQ> {         [        KP_Equal ] };
    key <I126> {         [       plusminus ] };
    key <PAUS> {
        type= "PC_CONTROL_LEVEL2",
        symbols[Group1]= [           Pause,           Break ]
    };
    key <I128> {         [     XF86LaunchA ] };
    key <I129> {         [      KP_Decimal,      KP_Decimal ] };
    key <HNGL> {         [          Hangul ] };
    key <HJCV> {         [    Hangul_Hanja ] };
    key <LWIN> {         [         Super_L ] };
    key <RWIN> {         [         Super_R ] };
    key <COMP> {         [            Menu ] };
    key <STOP> {         [          Cancel ] };
    key <AGAI> {         [            Redo ] };
    key <PROP> {         [        SunProps ] };
    key <UNDO> {         [            Undo ] };
    key <FRNT> {         [        SunFront ] };
    key <COPY> {         [        XF86Copy ] };
    key <OPEN> {         [        XF86Open ] };
    key <PAST> {         [       XF86Paste ] };
    key <FIND> {         [            Find ] };
    key  <CUT> {         [         XF86Cut ] };
    key <HELP> {         [            Help ] };
    key <I147> {         [      XF86MenuKB ] };
    key <I148> {         [  XF86Calculator ] };
    key <I150> {         [       XF86Sleep ] };
    key <I151> {         [      XF86WakeUp ] };
    key <I152> {         [    XF86Explorer ] };
    key <I153> {         [        XF86Send ] };
    key <I155> {         [        XF86Xfer ] };
    key <I156> {         [     XF86Launch1 ] };
    key <I157> {         [     XF86Launch2 ] };
    key <I158> {         [         XF86WWW ] };
    key <I159> {         [         XF86DOS ] };
    key <I160> {         [ XF86ScreenSaver ] };
    key <I161> {         [ XF86RotateWindows ] };
    key <I162> {         [    XF86TaskPane ] };
    key <I163> {         [        XF86Mail ] };
    key <I164> {         [   XF86Favorites ] };
    key <I165> {         [  XF86MyComputer ] };
    key <I166> {         [        XF86Back ] };
    key <I167> {         [     XF86Forward ] };
    key <I169> {         [       XF86Eject ] };
    key <I170> {         [       XF86Eject,       XF86Eject ] };
    key <I171> {         [   XF86AudioNext ] };
    key <I172> {         [   XF86AudioPlay,  XF86AudioPause ] };
    key <I173> {         [   XF86AudioPrev ] };
    key <I174> {         [   XF86AudioStop,       XF86Eject ] };
    key <I175> {         [ XF86AudioRecord ] };
    key <I176> {         [ XF86AudioRewind ] };
    key <I177> {         [       XF86Phone ] };
    key <I179> {         [       XF86Tools ] };
    key <I180> {         [    XF86HomePage ] };
    key <I181> {         [      XF86Reload ] };
    key <I182> {         [       XF86Close ] };
    key <I185> {         [    XF86ScrollUp ] };
    key <I186> {         [  XF86ScrollDown ] };
    key <I187> {         [       parenleft ] };
    key <I188> {         [      parenright ] };
    key <I189> {         [         XF86New ] };
    key <I190> {         [            Redo ] };
    key <FK13> {         [       XF86Tools ] };
    key <FK14> {         [     XF86Launch5 ] };
    key <FK15> {         [     XF86Launch6 ] };
    key <FK16> {         [     XF86Launch7 ] };
    key <FK17> {         [     XF86Launch8 ] };
    key <FK18> {         [     XF86Launch9 ] };
    key <FK20> {         [ XF86AudioMicMute ] };
    key <FK21> {         [ XF86TouchpadToggle ] };
    key <FK22> {         [  XF86TouchpadOn ] };
    key <FK23> {         [ XF86TouchpadOff ] };
    key <MDSW> {         [     Mode_switch ] };
    key  <ALT> {         [        NoSymbol,           Alt_L ] };
    key <META> {         [        NoSymbol,          Meta_L ] };
    key <SUPR> {         [        NoSymbol,         Super_L ] };
    key <HYPR> {         [        NoSymbol,         Hyper_L ] };
    key <I208> {         [   XF86AudioPlay ] };
    key <I209> {         [  XF86AudioPause ] };
    key <I210> {         [     XF86Launch3 ] };
    key <I211> {         [     XF86Launch4 ] };
    key <I212> {         [     XF86LaunchB ] };
    key <I213> {         [     XF86Suspend ] };
    key <I214> {         [       XF86Close ] };
    key <I215> {         [   XF86AudioPlay ] };
    key <I216> {         [ XF86AudioForward ] };
    key <I218> {         [           Print ] };
    key <I220> {         [      XF86WebCam ] };
    key <I223> {         [        XF86Mail ] };
    key <I224> {         [   XF86Messenger ] };
    key <I225> {         [      XF86Search ] };
    key <I226> {         [          XF86Go ] };
    key <I227> {         [     XF86Finance ] };
    key <I228> {         [        XF86Game ] };
    key <I229> {         [        XF86Shop ] };
    key <I231> {         [          Cancel ] };
    key <I232> {         [ XF86MonBrightnessDown ] };
    key <I233> {         [ XF86MonBrightnessUp ] };
    key <I234> {         [  XF86AudioMedia ] };
    key <I235> {         [     XF86Display ] };
    key <I236> {         [ XF86KbdLightOnOff ] };
    key <I237> {         [ XF86KbdBrightnessDown ] };
    key <I238> {         [ XF86KbdBrightnessUp ] };
    key <I239> {         [        XF86Send ] };
    key <I240> {         [       XF86Reply ] };
    key <I241> {         [ XF86MailForward ] };
    key <I242> {         [        XF86Save ] };
    key <I243> {         [   XF86Documents ] };
    key <I244> {         [     XF86Battery ] };
    key <I245> {         [   XF86Bluetooth ] };
    key <I246> {         [        XF86WLAN ] };
    modifier_map Control { <LCTL> };
    modifier_map Shift { <LFSH> };
    modifier_map Shift { <RTSH> };
    modifier_map Mod1 { <LALT> };
    modifier_map Lock { <CAPS> };
    modifier_map Mod2 { <NMLK> };
    modifier_map Mod5 { <LVL3> };
    modifier_map Control { <RCTL> };
    modifier_map Mod4 { <LWIN> };
    modifier_map Mod4 { <RWIN> };
    modifier_map Mod5 { <MDSW> };
    modifier_map Mod1 { <META> };
    modifier_map Mod4 { <SUPR> };
    modifier_map Mod4 { <HYPR> };
};

xkb_geometry "pc(pc105)" {

    width=       470;
    height=      180;

    alias <AC00> = <CAPS>;
    alias <AA00> = <LCTL>;

    baseColor=   "white";
    labelColor=  "black";
    xfont=       "-*-helvetica-medium-r-normal--*-120-*-*-*-*-iso8859-1";
    description= "Generic 105";

    shape "NORM" {
        corner= 1,
        { [  18,  18 ] },
        { [   2,   1 ], [  16,  16 ] }
    };
    shape "BKSP" {
        corner= 1,
        { [  38,  18 ] },
        { [   2,   1 ], [  36,  16 ] }
    };
    shape "TABK" {
        corner= 1,
        { [  28,  18 ] },
        { [   2,   1 ], [  26,  16 ] }
    };
    shape "BKSL" {
        corner= 1,
        { [  28,  18 ] },
        { [   2,   1 ], [  26,  16 ] }
    };
    shape "RTRN" {
        corner= 1,
        { [   0,   0 ], [  28,   0 ], [  28,  37 ], [   5,  37 ],
          [   5,  18 ], [   0,  18 ] },
        { [   2,   1 ], [  26,   1 ], [  26,  35 ], [   7,  35 ],
          [   7,  16 ], [   2,  16 ] },
        approx= { [   5,   0 ], [  28,  37 ] }
    };
    shape "CAPS" {
        corner= 1,
        { [  33,  18 ] },
        { [   2,   1 ], [  31,  16 ] }
    };
    shape "LFSH" {
        corner= 1,
        { [  25,  18 ] },
        { [   2,   1 ], [  23,  16 ] }
    };
    shape "RTSH" {
        corner= 1,
        { [  50,  18 ] },
        { [   2,   1 ], [  48,  16 ] }
    };
    shape "MODK" {
        corner= 1,
        { [  27,  18 ] },
        { [   2,   1 ], [  25,  16 ] }
    };
    shape "SMOD" {
        corner= 1,
        { [  23,  18 ] },
        { [   2,   1 ], [  21,  16 ] }
    };
    shape "SPCE" {
        corner= 1,
        { [ 113,  18 ] },
        { [   2,   1 ], [ 111,  16 ] }
    };
    shape "KP0" {
        corner= 1,
        { [  37,  18 ] },
        { [   2,   1 ], [  35,  16 ] }
    };
    shape "KPAD" {
        corner= 1,
        { [  18,  37 ] },
        { [   2,   1 ], [  16,  35 ] }
    };
    shape "LEDS" { { [  75,  20 ] } };
    shape "LED" { { [   5,   1 ] } };
    section "Function" {
        key.color= "grey20";
        priority=  7;
        top=       22;
        left=      19;
        width=     351;
        height=    19;
        row {
            top=  1;
            left= 1;
            keys {
                {  <ESC>, "NORM",   1 },
                { <FK01>, "NORM",  20, color="white" },
                { <FK02>, "NORM",   1, color="white" },
                { <FK03>, "NORM",   1, color="white" },
                { <FK04>, "NORM",   1, color="white" },
                { <FK05>, "NORM",  11, color="white" },
                { <FK06>, "NORM",   1, color="white" },
                { <FK07>, "NORM",   1, color="white" },
                { <FK08>, "NORM",   1, color="white" },
                { <FK09>, "NORM",  11, color="white" },
                { <FK10>, "NORM",   1, color="white" },
                { <FK11>, "NORM",   1, color="white" },
                { <FK12>, "NORM",   1, color="white" },
                { <PRSC>, "NORM",   8, color="white" },
                { <SCLK>, "NORM",   1, color="white" },
                { <PAUS>, "NORM",   1, color="white" }
            };
        };
    }; // End of "Function" section

    section "Alpha" {
        key.color= "white";
        priority=  8;
        top=       61;
        left=      19;
        width=     287;
        height=    95;
        row {
            top=  1;
            left= 1;
            keys {
                { <TLDE>, "NORM",   1 }, { <AE01>, "NORM",   1 },
                { <AE02>, "NORM",   1 }, { <AE03>, "NORM",   1 },
                { <AE04>, "NORM",   1 }, { <AE05>, "NORM",   1 },
                { <AE06>, "NORM",   1 }, { <AE07>, "NORM",   1 },
                { <AE08>, "NORM",   1 }, { <AE09>, "NORM",   1 },
                { <AE10>, "NORM",   1 }, { <AE11>, "NORM",   1 },
                { <AE12>, "NORM",   1 },
                { <BKSP>, "BKSP",   1, color="grey20" }
            };
        };
        row {
            top=  20;
            left= 1;
            keys {
                {  <TAB>, "TABK",   1, color="grey20" },
                { <AD01>, "NORM",   1 }, { <AD02>, "NORM",   1 },
                { <AD03>, "NORM",   1 }, { <AD04>, "NORM",   1 },
                { <AD05>, "NORM",   1 }, { <AD06>, "NORM",   1 },
                { <AD07>, "NORM",   1 }, { <AD08>, "NORM",   1 },
                { <AD09>, "NORM",   1 }, { <AD10>, "NORM",   1 },
                { <AD11>, "NORM",   1 }, { <AD12>, "NORM",   1 },
                { <RTRN>, "RTRN",   1, color="grey20" }
            };
        };
        row {
            top=  39;
            left= 1;
            keys {
                { <CAPS>, "CAPS",   1, color="grey20" },
                { <AC01>, "NORM",   1 }, { <AC02>, "NORM",   1 },
                { <AC03>, "NORM",   1 }, { <AC04>, "NORM",   1 },
                { <AC05>, "NORM",   1 }, { <AC06>, "NORM",   1 },
                { <AC07>, "NORM",   1 }, { <AC08>, "NORM",   1 },
                { <AC09>, "NORM",   1 }, { <AC10>, "NORM",   1 },
                { <AC11>, "NORM",   1 }, { <BKSL>, "NORM",   1 }
            };
        };
        row {
            top=  58;
            left= 1;
            keys {
                { <LFSH>, "LFSH",   1, color="grey20" },
                { <LSGT>, "NORM",   1 }, { <AB01>, "NORM",   1 },
                { <AB02>, "NORM",   1 }, { <AB03>, "NORM",   1 },
                { <AB04>, "NORM",   1 }, { <AB05>, "NORM",   1 },
                { <AB06>, "NORM",   1 }, { <AB07>, "NORM",   1 },
                { <AB08>, "NORM",   1 }, { <AB09>, "NORM",   1 },
                { <AB10>, "NORM",   1 },
                { <RTSH>, "RTSH",   1, color="grey20" }
            };
        };
        row {
            top=  77;
            left= 1;
            keys {
                { <LCTL>, "MODK",   1, color="grey20" },
                { <LWIN>, "SMOD",   1, color="grey20" },
                { <LALT>, "SMOD",   1, color="grey20" },
                { <SPCE>, "SPCE",   1 },
                { <RALT>, "SMOD",   1, color="grey20" },
                { <RWIN>, "SMOD",   1, color="grey20" },
                { <MENU>, "SMOD",   1, color="grey20" },
                { <RCTL>, "SMOD",   1, color="grey20" }
            };
        };
    }; // End of "Alpha" section

    section "Editing" {
        key.color= "grey20";
        priority=  9;
        top=       61;
        left=      312;
        width=     58;
        height=    95;
        row {
            top=  1;
            left= 1;
            keys {
                {  <INS>, "NORM",   1 }, { <HOME>, "NORM",   1 },
                { <PGUP>, "NORM",   1 }
            };
        };
        row {
            top=  20;
            left= 1;
            keys {
                { <DELE>, "NORM",   1 }, {  <END>, "NORM",   1 },
                { <PGDN>, "NORM",   1 }
            };
        };
        row {
            top=  58;
            left= 20;
            keys {
                {   <UP>, "NORM",   1 }
            };
        };
        row {
            top=  77;
            left= 1;
            keys {
                { <LEFT>, "NORM",   1 }, { <DOWN>, "NORM",   1 },
                { <RGHT>, "NORM",   1 }
            };
        };
    }; // End of "Editing" section

    section "Keypad" {
        key.color= "grey20";
        priority=  10;
        top=       61;
        left=      376;
        width=     77;
        height=    95;
        row {
            top=  1;
            left= 1;
            keys {
                { <NMLK>, "NORM",   1 }, { <KPDV>, "NORM",   1 },
                { <KPMU>, "NORM",   1 }, { <KPSU>, "NORM",   1 }
            };
        };
        row {
            top=  20;
            left= 1;
            keys {
                {  <KP7>, "NORM",   1, color="white" },
                {  <KP8>, "NORM",   1, color="white" },
                {  <KP9>, "NORM",   1, color="white" },
                { <KPAD>, "KPAD",   1 }
            };
        };
        row {
            top=  39;
            left= 1;
            keys {
                {  <KP4>, "NORM",   1, color="white" },
                {  <KP5>, "NORM",   1, color="white" },
                {  <KP6>, "NORM",   1, color="white" }
            };
        };
        row {
            top=  58;
            left= 1;
            keys {
                {  <KP1>, "NORM",   1, color="white" },
                {  <KP2>, "NORM",   1, color="white" },
                {  <KP3>, "NORM",   1, color="white" },
                { <KPEN>, "KPAD",   1 }
            };
        };
        row {
            top=  77;
            left= 1;
            keys {
                {  <KP0>, "KP0",   1, color="white" },
                { <KPDL>, "NORM",   1, color="white" }
            };
        };
    }; // End of "Keypad" section

    solid "LedPanel" {
        top=      22;
        left=     377;
        priority= 0;
        color= "grey10";
        shape= "LEDS";
    };
    indicator "Num Lock" {
        top=      37;
        left=     382;
        priority= 1;
        onColor= "green";
        offColor= "green30";
        shape= "LED";
    };
    indicator "Caps Lock" {
        top=      37;
        left=     407;
        priority= 2;
        onColor= "green";
        offColor= "green30";
        shape= "LED";
    };
    indicator "Scroll Lock" {
        top=      37;
        left=     433;
        priority= 3;
        onColor= "green";
        offColor= "green30";
        shape= "LED";
    };
    text "NumLockLabel" {
        top=      25;
        left=     378;
        priority= 4;
        width=  19.8;
        height=  10;
        XFont= "-*-helvetica-medium-r-normal--*-120-*-*-*-*-iso8859-1";
        text=  "Num\nLock";
    };
    text "CapsLockLabel" {
        top=      25;
        left=     403;
        priority= 5;
        width=  26.4;
        height=  10;
        XFont= "-*-helvetica-medium-r-normal--*-120-*-*-*-*-iso8859-1";
        text=  "Caps\nLock";
    };
    text "ScrollLockLabel" {
        top=      25;
        left=     428;
        priority= 6;
        width=  39.6;
        height=  10;
        XFont= "-*-helvetica-medium-r-normal--*-120-*-*-*-*-iso8859-1";
        text=  "Scroll\nLock";
    };
};

};
"""

sample_keymap_bytes = sample_keymap_string.encode('ascii')

# Compose files are encoded in whatever locale they are intended to be
# used in. This sample data is for UTF-8.
sample_compose_bytes = r"""# UTF-8 (Unicode) Compose sequences
#
# Spacing versions of accents (mostly)
<dead_tilde> <space>			: "~"	asciitilde # TILDE
<dead_tilde> <dead_tilde>		: "~"	asciitilde # TILDE
<Multi_key> <minus> <space>		: "~"	asciitilde # TILDE
<Multi_key> <space> <minus>		: "~"	asciitilde # TILDE
<dead_acute> <space>			: "'"	apostrophe # APOSTROPHE
<dead_acute> <dead_acute>		: "´"	acute # ACUTE ACCENT
<Multi_key> <apostrophe> <apostrophe>	: "´"	acute # ACUTE ACCENT
<dead_grave> <space>			: "`"	grave # GRAVE ACCENT
<dead_grave> <dead_grave>		: "`"	grave # GRAVE ACCENT
<dead_circumflex> <space>		: "^"	asciicircum # CIRCUMFLEX ACCENT
<dead_circumflex> <dead_circumflex>	: "^"	asciicircum # CIRCUMFLEX ACCENT
<Multi_key> <greater> <space>		: "^"	asciicircum # CIRCUMFLEX ACCENT
<Multi_key> <space> <greater>		: "^"	asciicircum # CIRCUMFLEX ACCENT
<dead_abovering> <space>		: "°"	degree # DEGREE SIGN
<dead_abovering> <dead_abovering>	: "°"	degree # DEGREE SIGN
<Multi_key> <o> <o>			: "°"	degree # DEGREE SIGN
<Multi_key> <asterisk> <0>		: "°"	degree # DEGREE SIGN
<Multi_key> <0> <asterisk>		: "°"	degree # DEGREE SIGN
<dead_macron> <space>			: "¯"	macron # MACRON
<dead_macron> <dead_macron>		: "¯"	macron # MACRON
<Multi_key> <minus> <asciicircum>	: "¯"	macron # MACRON
<Multi_key> <underscore> <space>	: "¯"	macron # MACRON
<Multi_key> <space> <underscore>	: "¯"	macron # MACRON
<Multi_key> <underscore> <underscore>	: "¯"	macron # MACRON
<Multi_key> <underscore> <asciicircum>	: "¯"	macron # MACRON
<dead_breve> <space>			: "˘"	breve # BREVE
<dead_breve> <dead_breve>		: "˘"	breve # BREVE
<Multi_key> <parenleft> <space>		: "˘"	breve # BREVE
<Multi_key> <space> <parenleft>		: "˘"	breve # BREVE
<dead_abovedot> <space>			: "˙"	abovedot # DOT ABOVE
<dead_abovedot> <dead_abovedot>		: "˙"	abovedot # DOT ABOVE
<Multi_key> <period> <space>		: "˙"	abovedot # DOT ABOVE
<dead_diaeresis> <dead_diaeresis>	: "¨"	diaeresis # DIAERESIS
<Multi_key> <quotedbl> <space>		: "¨"	diaeresis # DIAERESIS
<Multi_key> <quotedbl> <quotedbl>	: "¨"	diaeresis # DIAERESIS
<dead_diaeresis> <space>		: "\""	quotedbl # QUOTATION MARK
<dead_doubleacute> <space>		: "˝"	U2dd # DOUBLE ACUTE ACCENT
<dead_doubleacute> <dead_doubleacute>	: "˝"	U2dd # DOUBLE ACUTE ACCENT
<dead_caron> <space>			: "ˇ"	caron # CARON
<dead_caron> <dead_caron>		: "ˇ"	caron # CARON
<Multi_key> <less> <space>		: "ˇ"	caron # CARON
<Multi_key> <space> <less>		: "ˇ"	caron # CARON
<dead_cedilla> <space>			: "¸"	cedilla # CEDILLA
<dead_cedilla> <dead_cedilla>		: "¸"	cedilla # CEDILLA
<Multi_key> <comma> <space>		: "¸"	cedilla # CEDILLA
<Multi_key> <space> <comma>		: "¸"	cedilla # CEDILLA
<Multi_key> <comma> <comma>		: "¸"	cedilla # CEDILLA
<dead_ogonek> <space>			: "˛"	ogonek # OGONEK
<dead_ogonek> <dead_ogonek>		: "˛"	ogonek # OGONEK
<Multi_key> <semicolon> <space>		: "˛"	ogonek # OGONEK
<dead_iota> <space>			: "ͺ"	U37a # GREEK YPOGEGRAMMENI
<dead_iota> <dead_iota>			: "ͺ"	U37a # GREEK YPOGEGRAMMENI
# ASCII characters that may be difficult to access on some keyboards.
<Multi_key> <plus> <plus>		: "#"	numbersign # NUMBER SIGN
<Multi_key> <A> <T>			: "@"	at # COMMERCIAL AT
<Multi_key> <parenleft> <parenleft>	: "["	bracketleft # LEFT SQUARE BRACKET
<Multi_key> <parenright> <parenright>	: "]"	bracketright # RIGHT SQUARE BRACKET
<Multi_key> <slash> <slash>		: "\\"	backslash # REVERSE SOLIDUS
<Multi_key> <slash> <less>		: "\\"	backslash # REVERSE SOLIDUS
<Multi_key> <parenleft> <minus>		: "{"	braceleft # LEFT CURLY BRACKET
<Multi_key> <minus> <parenleft>		: "{"	braceleft # LEFT CURLY BRACKET
<Multi_key> <parenright> <minus>	: "}"	braceright # RIGHT CURLY BRACKET
<Multi_key> <minus> <parenright>	: "}"	braceright # RIGHT CURLY BRACKET
<Multi_key> <slash> <asciicircum>	: "|"	bar # VERTICAL LINE
<Multi_key> <asciicircum> <slash>	: "|"	bar # VERTICAL LINE
<Multi_key> <V> <L>			: "|"	bar # VERTICAL LINE
<Multi_key> <L> <V>			: "|"	bar # VERTICAL LINE
<Multi_key> <v> <l>			: "|"	bar # VERTICAL LINE
<Multi_key> <l> <v>			: "|"	bar # VERTICAL LINE
<Multi_key> <L> <T>			: "<"	less # LESS-THAN
<Multi_key> <l> <t>			: "<"	less # LESS-THAN
<Multi_key> <G> <T>			: ">"	greater # GREATER-THAN
<Multi_key> <g> <t>			: ">"	greater # GREATER-THAN
# Two special spaces
<Multi_key> <space> <space>		: " "	nobreakspace # NO-BREAK SPACE
<Multi_key> <space> <period>		: " "	U2008 # PUNCTUATION SPACE
<Multi_key> <o> <c>			: "©"	copyright # COPYRIGHT SIGN
<Multi_key> <O> <C>			: "©"	copyright # COPYRIGHT SIGN
<Multi_key> <C> <O>			: "©"	copyright # COPYRIGHT SIGN
<Multi_key> <o> <r>			: "®"	registered # REGISTERED SIGN
<Multi_key> <O> <R>			: "®"	registered # REGISTERED SIGN
<Multi_key> <R> <O>			: "®"	registered # REGISTERED SIGN
<Multi_key> <parenleft> <parenright> <parenright>: "🄯"	U1F12F # COPYLEFT SYMBOL
# Special punctuation
<Multi_key> <period> <period>		: "…"	ellipsis # HORIZONTAL ELLIPSIS
<Multi_key> <period> <minus>		: "·"	periodcentered # MIDDLE DOT
<Multi_key> <period> <asciicircum>	: "·"	periodcentered # MIDDLE DOT
<Multi_key> <asciicircum> <period>	: "·"	periodcentered # MIDDLE DOT
<dead_circumflex> <period>		: "·"	periodcentered # MIDDLE DOT
<Multi_key> <period> <equal>		: "•"	enfilledcircbullet # BULLET
<Multi_key> <exclam> <asciicircum>	: "¦"	brokenbar # BROKEN BAR
<Multi_key> <exclam> <exclam>		: "¡"	exclamdown # INVERTED EXCLAMATION MARK
<Multi_key> <plus> <minus>		: "±"	plusminus # PLUS-MINUS SIGN
<Multi_key> <minus> <plus>		: "±"	plusminus # PLUS-MINUS SIGN
<Multi_key> <question> <question>	: "¿"	questiondown # INVERTED QUESTION MARK
<Multi_key> <exclam> <question>		: "‽"	U203D # INTERROBANG
<Multi_key> <question> <exclam>		: "⸘"	U2E18 # INVERTED INTERROBANG
<Multi_key> <minus> <minus> <space>	: "­"	U00ad # SOFT HYPHEN
<Multi_key> <bar> <minus>		: "†"	U2020 # DAGGER
<Multi_key> <bar> <equal>		: "‡"	U2021 # DOUBLE DAGGER
<Multi_key> <percent> <o>		: "‰"	U2030 # PER MILLE SIGN
# Some ligatures
<Multi_key> <a> <e>			: "æ"	ae # LATIN SMALL LETTER AE
<Multi_key> <A> <E>			: "Æ"	AE # LATIN CAPITAL LETTER AE
<Multi_key> <o> <e>			: "œ"	oe # LATIN SMALL LIGATURE OE
<Multi_key> <O> <E>			: "Œ"	OE # LATIN CAPITAL LIGATURE OE
<Multi_key> <s> <s>			: "ß"	ssharp # LATIN SMALL LETTER SHARP S
<Multi_key> <S> <S>			: "ẞ"	U1e9e # LATIN CAPITAL LETTER SHARP S
<Multi_key> <f> <f>			: "ﬀ"	Ufb00 # LATIN SMALL LIGATURE FF
<Multi_key> <f> <i>			: "ﬁ"	Ufb01 # LATIN SMALL LIGATURE FI
<Multi_key> <f> <l>			: "ﬂ"	Ufb02 # LATIN SMALL LIGATURE FL
<Multi_key> <F> <i>			: "ﬃ"	Ufb03 # LATIN SMALL LIGATURE FFI
<Multi_key> <F> <l>			: "ﬄ"	Ufb04 # LATIN SMALL LIGATURE FFL
<Multi_key> <i> <j>			: "ĳ"	U0133 # LATIN SMALL LIGATURE IJ
<Multi_key> <I> <j>			: "Ĳ"	U0132 # LATIN CAPITAL LIGATURE IJ
<Multi_key> <I> <J>			: "Ĳ"	U0132 # LATIN CAPITAL LIGATURE IJ
# Quotation marks
<Multi_key> <less> <less>		: "«"	guillemotleft # LEFT-POINTING DOUBLE ANGLE QUOTATION MARK
<Multi_key> <greater> <greater>		: "»"	guillemotright # RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK
<Multi_key> <period> <less>		: "‹"	U2039 # SINGLE LEFT-POINTING ANGLE QUOTATION MARK
<Multi_key> <period> <greater>		: "›"	U203a # SINGLE RIGHT-POINTING ANGLE QUOTATION MARK
<Multi_key> <less> <apostrophe>		: "‘"	U2018 # LEFT SINGLE QUOTATION MARK
<Multi_key> <apostrophe> <less>		: "‘"	U2018 # LEFT SINGLE QUOTATION MARK
<Multi_key> <greater> <apostrophe>	: "’"	U2019 # RIGHT SINGLE QUOTATION MARK
<Multi_key> <apostrophe> <greater>	: "’"	U2019 # RIGHT SINGLE QUOTATION MARK
<Multi_key> <comma> <apostrophe>	: "‚"	U201a # SINGLE LOW-9 QUOTATION MARK
<Multi_key> <apostrophe> <comma>	: "‚"	U201a # SINGLE LOW-9 QUOTATION MARK
<Multi_key> <less> <quotedbl>		: "“"	U201c # LEFT DOUBLE QUOTATION MARK
<Multi_key> <quotedbl> <less>		: "“"	U201c # LEFT DOUBLE QUOTATION MARK
<Multi_key> <greater> <quotedbl>	: "”"	U201d # RIGHT DOUBLE QUOTATION MARK
<Multi_key> <quotedbl> <greater>	: "”"	U201d # RIGHT DOUBLE QUOTATION MARK
<Multi_key> <comma> <quotedbl>		: "„"	U201e # DOUBLE LOW-9 QUOTATION MARK
<Multi_key> <quotedbl> <comma>		: "„"	U201e # DOUBLE LOW-9 QUOTATION MARK
# Currencies
<Multi_key> <S> <bar>			: "$"	dollar # DOLLAR SIGN
<Multi_key> <bar> <S>			: "$"	dollar # DOLLAR SIGN
<Multi_key> <c> <bar>			: "¢"	cent # CENT SIGN
<Multi_key> <bar> <c>			: "¢"	cent # CENT SIGN
<Multi_key> <c> <slash>			: "¢"	cent # CENT SIGN
<Multi_key> <slash> <c>			: "¢"	cent # CENT SIGN
<Multi_key> <L> <minus>			: "£"	sterling # POUND SIGN
<Multi_key> <minus> <L>			: "£"	sterling # POUND SIGN
<Multi_key> <l> <minus>			: "£"	sterling # POUND SIGN
<Multi_key> <minus> <l>			: "£"	sterling # POUND SIGN
<Multi_key> <Y> <equal>			: "¥"	yen # YEN SIGN
<Multi_key> <equal> <Y>			: "¥"	yen # YEN SIGN
<Multi_key> <y> <equal>			: "¥"	yen # YEN SIGN
<Multi_key> <equal> <y>			: "¥"	yen # YEN SIGN
<Multi_key> <B> <bar>			: "฿"	U0e3f # THAI CURRENCY SYMBOL BAHT
<Multi_key> <bar> <B>			: "฿"	U0e3f # THAI CURRENCY SYMBOL BAHT
<Multi_key> <C> <E>			: "₠"	U20a0 # EURO-CURRENCY SIGN
<Multi_key> <C> <slash>			: "₡"	U20a1 # COLON SIGN
<Multi_key> <slash> <C>			: "₡"	U20a1 # COLON SIGN
<Multi_key> <C> <r>			: "₢"	U20a2 # CRUZEIRO SIGN
<Multi_key> <F> <r>			: "₣"	U20a3 # FRENCH FRANC SIGN
<Multi_key> <L> <equal>			: "₤"	U20a4 # LIRA SIGN
<Multi_key> <equal> <L>			: "₤"	U20a4 # LIRA SIGN
<Multi_key> <m> <slash>			: "₥"	U20a5 # MILL SIGN
<Multi_key> <slash> <m>			: "₥"	U20a5 # MILL SIGN
<Multi_key> <N> <equal>			: "₦"	U20a6 # NAIRA SIGN
<Multi_key> <equal> <N>			: "₦"	U20a6 # NAIRA SIGN
<Multi_key> <P> <t>			: "₧"	U20a7 # PESETA SIGN
<Multi_key> <R> <s>			: "₨"	U20a8 # RUPEE SIGN
<Multi_key> <W> <equal>			: "₩"	U20a9 # WON SIGN
<Multi_key> <equal> <W>			: "₩"	U20a9 # WON SIGN
# "₪" U20aa NEW SHEQEL SIGN
<Multi_key> <d> <equal>			: "₫"	U20ab # DONG SIGN
<Multi_key> <equal> <d>			: "₫"	U20ab # DONG SIGN
<Multi_key> <C> <equal>			: "€"	EuroSign # EURO SIGN
<Multi_key> <equal> <C>			: "€"	EuroSign # EURO SIGN
<Multi_key> <c> <equal>			: "€"	EuroSign # EURO SIGN
<Multi_key> <equal> <c>			: "€"	EuroSign # EURO SIGN
<Multi_key> <E> <equal>			: "€"	EuroSign # EURO SIGN
<Multi_key> <equal> <E>			: "€"	EuroSign # EURO SIGN
<Multi_key> <e> <equal>			: "€"	EuroSign # EURO SIGN
<Multi_key> <equal> <e>			: "€"	EuroSign # EURO SIGN
<Multi_key> <Cyrillic_ES> <equal>	: "€"	EuroSign # EURO SIGN
<Multi_key> <equal> <Cyrillic_ES>	: "€"	EuroSign # EURO SIGN
<Multi_key> <Cyrillic_IE> <equal>	: "€"	EuroSign # EURO SIGN
<Multi_key> <equal> <Cyrillic_IE>	: "€"	EuroSign # EURO SIGN
<Multi_key> <K> <minus>			: "₭"	U20ad # KIP SIGN
<Multi_key> <minus> <K>			: "₭"	U20ad # KIP SIGN
<Multi_key> <T> <equal>			: "₮"	U20ae # TUGRIK SIGN
<Multi_key> <equal> <T>			: "₮"	U20ae # TUGRIK SIGN
# "₱" U20b1 PESO SIGN
<Multi_key> <G> <bar>			: "₲"	U20b2 # GUARANI SIGN
<Multi_key> <bar> <G>			: "₲"	U20b2 # GUARANI SIGN
# "₴" U20b4 HRYVNIA SIGN
<Multi_key> <C> <bar>			: "₵"	U20b5 # CEDI SIGN
<Multi_key> <bar> <C>			: "₵"	U20b5 # CEDI SIGN
<Multi_key> <R> <equal>			: "₹"	U20b9 # INDIAN RUPEE SIGN
<Multi_key> <equal> <R>			: "₹"	U20b9 # INDIAN RUPEE SIGN
<Multi_key> <r> <equal>			: "₹"	U20b9 # INDIAN RUPEE SIGN
<Multi_key> <equal> <r>			: "₹"	U20b9 # INDIAN RUPEE SIGN
<Multi_key> <P> <equal>			: "₽"	U20bd # ROUBLE SIGN
<Multi_key> <equal> <P>			: "₽"	U20bd # ROUBLE SIGN
<Multi_key> <p> <equal>			: "₽"	U20bd # ROUBLE SIGN
<Multi_key> <equal> <p>			: "₽"	U20bd # ROUBLE SIGN
<Multi_key> <Cyrillic_ZE> <equal>	: "₽"	U20bd # ROUBLE SIGN
<Multi_key> <equal> <Cyrillic_ZE>	: "₽"	U20bd # ROUBLE SIGN
<Multi_key> <Cyrillic_ze> <equal>	: "₽"	U20bd # ROUBLE SIGN
<Multi_key> <equal> <Cyrillic_ze>	: "₽"	U20bd # ROUBLE SIGN
# Dashes
<Multi_key> <minus> <minus> <period>	: "–"	U2013 # EN DASH
<Multi_key> <minus> <minus> <minus>	: "—"	U2014 # EM DASH
# Musical alterations
<Multi_key> <numbersign> <q>		: "♩"	U2669 # QUARTER NOTE
<Multi_key> <numbersign> <e>		: "♪"	U266a # EIGHTH NOTE
<Multi_key> <numbersign> <E>		: "♫"	U266b # BEAMED EIGHTH NOTES
<Multi_key> <numbersign> <S>		: "♬"	U266c # BEAMED SIXTEENTH NOTES
<Multi_key> <numbersign> <b>		: "♭"	U266d # MUSIC FLAT SIGN
<Multi_key> <numbersign> <f>		: "♮"	U266e # MUSIC NATURAL SIGN
<Multi_key> <numbersign> <numbersign>	: "♯"	U266f # MUSIC SHARP SIGN
# Other symbols
<Multi_key> <s> <o>			: "§"	section # SECTION SIGN
<Multi_key> <o> <s>			: "§"	section # SECTION SIGN
<Multi_key> <S> <O>			: "§"	section # SECTION SIGN
<Multi_key> <O> <S>			: "§"	section # SECTION SIGN
<Multi_key> <s> <exclam>		: "§"	section # SECTION SIGN
<Multi_key> <S> <exclam>		: "§"	section # SECTION SIGN
<Multi_key> <Cyrillic_pe> <Cyrillic_a>	: "§"	section # SECTION SIGN
<Multi_key> <p> <exclam>		: "¶"	paragraph # PILCROW SIGN
<Multi_key> <P> <exclam>		: "¶"	paragraph # PILCROW SIGN
<Multi_key> <P> <P>			: "¶"	paragraph # PILCROW SIGN
<Multi_key> <o> <x>			: "¤"	currency # CURRENCY SIGN
<Multi_key> <x> <o>			: "¤"	currency # CURRENCY SIGN
<Multi_key> <O> <X>			: "¤"	currency # CURRENCY SIGN
<Multi_key> <X> <O>			: "¤"	currency # CURRENCY SIGN
<Multi_key> <N> <o>			: "№"	numerosign # NUMERO SIGN
<Multi_key> <N> <O>			: "№"	numerosign # NUMERO SIGN
<Multi_key> <Cyrillic_EN> <Cyrillic_o>	: "№"	numerosign # NUMERO SIGN
<Multi_key> <Cyrillic_EN> <Cyrillic_O>	: "№"	numerosign # NUMERO SIGN
<Multi_key> <question> <backslash>	: "☭"	U262D # HAMMER AND SICKLE
<Multi_key> <backslash> <question>	: "☭"	U262D # HAMMER AND SICKLE
<Multi_key> <O> <Y>			: "☮"	U262E # PEACE SYMBOL
<Multi_key> <O> <A>			: "Ⓐ"	U24B6 # CIRCLED LATIN CAPITAL LETTER A
<Multi_key> <less> <3>			: "♥"	U2665 # BLACK HEART SUIT
<Multi_key> <colon> <parenright>	: "☺"	U263A # WHITE SMILING FACE
<Multi_key> <colon> <parenleft>		: "☹"	U2639 # WHITE FROWNING FACE
<Multi_key> <backslash> <o> <slash>	: "🙌"	U1F64C # PERSON RAISING BOTH HANDS IN CELEBRATION
<Multi_key> <p> <o> <o>			: "💩"	U1F4A9 # PILE OF POO
<Multi_key> <F> <U>			: "🖕"	U1F595 # REVERSED HAND WITH MIDDLE FINGER EXTENDED
<Multi_key> <L> <L> <A> <P>		: "🖖"	U1F596 # RAISED HAND WITH PART BETWEEN MIDDLE AND RING FINGERS
# Latin-1 Supplement
<Multi_key> <comma> <minus>		: "¬"	notsign # NOT SIGN
<Multi_key> <minus> <comma>		: "¬"	notsign # NOT SIGN
<dead_circumflex> <Multi_key> <underscore> <a>	: "ª"	ordfeminine # FEMININE ORDINAL INDICATOR
<Multi_key> <asciicircum> <underscore> <a>	: "ª"	ordfeminine # FEMININE ORDINAL INDICATOR
<dead_circumflex> <Multi_key> <underscore> <o>	: "º"	masculine # MASCULINE ORDINAL INDICATOR
<Multi_key> <asciicircum> <underscore> <o>	: "º"	masculine # MASCULINE ORDINAL INDICATOR
<dead_circumflex> <1>			: "¹"	onesuperior # SUPERSCRIPT ONE
<Multi_key> <asciicircum> <1>		: "¹"	onesuperior # SUPERSCRIPT ONE
<Multi_key> <1> <asciicircum>		: "¹"	onesuperior # SUPERSCRIPT ONE
<dead_circumflex> <KP_1>		: "¹"	onesuperior # SUPERSCRIPT ONE
<Multi_key> <asciicircum> <KP_1>	: "¹"	onesuperior # SUPERSCRIPT ONE
<dead_circumflex> <2>			: "²"	twosuperior # SUPERSCRIPT TWO
<Multi_key> <asciicircum> <2>		: "²"	twosuperior # SUPERSCRIPT TWO
<Multi_key> <2> <asciicircum>		: "²"	twosuperior # SUPERSCRIPT TWO
<dead_circumflex> <KP_2>		: "²"	twosuperior # SUPERSCRIPT TWO
<Multi_key> <asciicircum> <KP_2>	: "²"	twosuperior # SUPERSCRIPT TWO
<dead_circumflex> <3>			: "³"	threesuperior # SUPERSCRIPT THREE
<Multi_key> <asciicircum> <3>		: "³"	threesuperior # SUPERSCRIPT THREE
<Multi_key> <3> <asciicircum>		: "³"	threesuperior # SUPERSCRIPT THREE
<dead_circumflex> <KP_3>		: "³"	threesuperior # SUPERSCRIPT THREE
<Multi_key> <asciicircum> <KP_3>	: "³"	threesuperior # SUPERSCRIPT THREE
<Multi_key> <m> <u>			: "µ"	mu # MICRO SIGN
<Multi_key> <slash> <u>			: "µ"	mu # MICRO SIGN
<Multi_key> <u> <slash>			: "µ"	mu # MICRO SIGN
<Multi_key> <1> <4>			: "¼"	onequarter # VULGAR FRACTION ONE QUARTER
<Multi_key> <1> <2>			: "½"	onehalf # VULGAR FRACTION ONE HALF
<Multi_key> <3> <4>			: "¾"	threequarters # VULGAR FRACTION THREE QUARTERS
<dead_grave> <A>			: "À"	Agrave # LATIN CAPITAL LETTER A WITH GRAVE
<Multi_key> <grave> <A>			: "À"	Agrave # LATIN CAPITAL LETTER A WITH GRAVE
<Multi_key> <A> <grave>			: "À"	Agrave # LATIN CAPITAL LETTER A WITH GRAVE
<dead_acute> <A>			: "Á"	Aacute # LATIN CAPITAL LETTER A WITH ACUTE
<Multi_key> <acute> <A>			: "Á"	Aacute # LATIN CAPITAL LETTER A WITH ACUTE
<Multi_key> <A> <acute>			: "Á"	Aacute # LATIN CAPITAL LETTER A WITH ACUTE
<Multi_key> <apostrophe> <A>		: "Á"	Aacute # LATIN CAPITAL LETTER A WITH ACUTE
<Multi_key> <A> <apostrophe>		: "Á"	Aacute # LATIN CAPITAL LETTER A WITH ACUTE
<dead_circumflex> <A>			: "Â"	Acircumflex # LATIN CAPITAL LETTER A WITH CIRCUMFLEX
<Multi_key> <asciicircum> <A>		: "Â"	Acircumflex # LATIN CAPITAL LETTER A WITH CIRCUMFLEX
<Multi_key> <A> <asciicircum>		: "Â"	Acircumflex # LATIN CAPITAL LETTER A WITH CIRCUMFLEX
<Multi_key> <greater> <A>		: "Â"	Acircumflex # LATIN CAPITAL LETTER A WITH CIRCUMFLEX
<Multi_key> <A> <greater>		: "Â"	Acircumflex # LATIN CAPITAL LETTER A WITH CIRCUMFLEX
<dead_tilde> <A>			: "Ã"	Atilde # LATIN CAPITAL LETTER A WITH TILDE
<Multi_key> <asciitilde> <A>		: "Ã"	Atilde # LATIN CAPITAL LETTER A WITH TILDE
<Multi_key> <A> <asciitilde>		: "Ã"	Atilde # LATIN CAPITAL LETTER A WITH TILDE
<dead_diaeresis> <A>			: "Ä"	Adiaeresis # LATIN CAPITAL LETTER A WITH DIAERESIS
<Multi_key> <quotedbl> <A>		: "Ä"	Adiaeresis # LATIN CAPITAL LETTER A WITH DIAERESIS
<Multi_key> <A> <quotedbl>		: "Ä"	Adiaeresis # LATIN CAPITAL LETTER A WITH DIAERESIS
<Multi_key> <diaeresis> <A>		: "Ä"	Adiaeresis # LATIN CAPITAL LETTER A WITH DIAERESIS
<Multi_key> <A> <diaeresis>		: "Ä"	Adiaeresis # LATIN CAPITAL LETTER A WITH DIAERESIS
<dead_abovering> <A>			: "Å"	Aring # LATIN CAPITAL LETTER A WITH RING ABOVE
<Multi_key> <o> <A>			: "Å"	Aring # LATIN CAPITAL LETTER A WITH RING ABOVE
<Multi_key> <asterisk> <A>		: "Å"	Aring # LATIN CAPITAL LETTER A WITH RING ABOVE
<Multi_key> <A> <asterisk>		: "Å"	Aring # LATIN CAPITAL LETTER A WITH RING ABOVE
<Multi_key> <A> <A>			: "Å"	Aring # LATIN CAPITAL LETTER A WITH RING ABOVE
<dead_cedilla> <C>			: "Ç"	Ccedilla # LATIN CAPITAL LETTER C WITH CEDILLA
<Multi_key> <comma> <C>			: "Ç"	Ccedilla # LATIN CAPITAL LETTER C WITH CEDILLA
<Multi_key> <C> <comma>			: "Ç"	Ccedilla # LATIN CAPITAL LETTER C WITH CEDILLA
<Multi_key> <cedilla> <C>		: "Ç"	Ccedilla # LATIN CAPITAL LETTER C WITH CEDILLA
<dead_grave> <E>			: "È"	Egrave # LATIN CAPITAL LETTER E WITH GRAVE
<Multi_key> <grave> <E>			: "È"	Egrave # LATIN CAPITAL LETTER E WITH GRAVE
<Multi_key> <E> <grave>			: "È"	Egrave # LATIN CAPITAL LETTER E WITH GRAVE
<dead_acute> <E>			: "É"	Eacute # LATIN CAPITAL LETTER E WITH ACUTE
<Multi_key> <acute> <E>			: "É"	Eacute # LATIN CAPITAL LETTER E WITH ACUTE
<Multi_key> <E> <acute>			: "É"	Eacute # LATIN CAPITAL LETTER E WITH ACUTE
<Multi_key> <apostrophe> <E>		: "É"	Eacute # LATIN CAPITAL LETTER E WITH ACUTE
<Multi_key> <E> <apostrophe>		: "É"	Eacute # LATIN CAPITAL LETTER E WITH ACUTE
<dead_circumflex> <E>			: "Ê"	Ecircumflex # LATIN CAPITAL LETTER E WITH CIRCUMFLEX
<Multi_key> <asciicircum> <E>		: "Ê"	Ecircumflex # LATIN CAPITAL LETTER E WITH CIRCUMFLEX
<Multi_key> <E> <asciicircum>		: "Ê"	Ecircumflex # LATIN CAPITAL LETTER E WITH CIRCUMFLEX
<Multi_key> <greater> <E>		: "Ê"	Ecircumflex # LATIN CAPITAL LETTER E WITH CIRCUMFLEX
<Multi_key> <E> <greater>		: "Ê"	Ecircumflex # LATIN CAPITAL LETTER E WITH CIRCUMFLEX
<dead_diaeresis> <E>			: "Ë"	Ediaeresis # LATIN CAPITAL LETTER E WITH DIAERESIS
<Multi_key> <quotedbl> <E>		: "Ë"	Ediaeresis # LATIN CAPITAL LETTER E WITH DIAERESIS
<Multi_key> <E> <quotedbl>		: "Ë"	Ediaeresis # LATIN CAPITAL LETTER E WITH DIAERESIS
<Multi_key> <diaeresis> <E>		: "Ë"	Ediaeresis # LATIN CAPITAL LETTER E WITH DIAERESIS
<Multi_key> <E> <diaeresis>		: "Ë"	Ediaeresis # LATIN CAPITAL LETTER E WITH DIAERESIS
<dead_grave> <I>			: "Ì"	Igrave # LATIN CAPITAL LETTER I WITH GRAVE
<Multi_key> <grave> <I>			: "Ì"	Igrave # LATIN CAPITAL LETTER I WITH GRAVE
<Multi_key> <I> <grave>			: "Ì"	Igrave # LATIN CAPITAL LETTER I WITH GRAVE
<dead_acute> <I>			: "Í"	Iacute # LATIN CAPITAL LETTER I WITH ACUTE
<Multi_key> <acute> <I>			: "Í"	Iacute # LATIN CAPITAL LETTER I WITH ACUTE
<Multi_key> <I> <acute>			: "Í"	Iacute # LATIN CAPITAL LETTER I WITH ACUTE
<Multi_key> <apostrophe> <I>		: "Í"	Iacute # LATIN CAPITAL LETTER I WITH ACUTE
<Multi_key> <I> <apostrophe>		: "Í"	Iacute # LATIN CAPITAL LETTER I WITH ACUTE
<dead_circumflex> <I>			: "Î"	Icircumflex # LATIN CAPITAL LETTER I WITH CIRCUMFLEX
<Multi_key> <asciicircum> <I>		: "Î"	Icircumflex # LATIN CAPITAL LETTER I WITH CIRCUMFLEX
<Multi_key> <I> <asciicircum>		: "Î"	Icircumflex # LATIN CAPITAL LETTER I WITH CIRCUMFLEX
<Multi_key> <greater> <I>		: "Î"	Icircumflex # LATIN CAPITAL LETTER I WITH CIRCUMFLEX
<Multi_key> <I> <greater>		: "Î"	Icircumflex # LATIN CAPITAL LETTER I WITH CIRCUMFLEX
<dead_diaeresis> <I>			: "Ï"	Idiaeresis # LATIN CAPITAL LETTER I WITH DIAERESIS
<Multi_key> <quotedbl> <I>		: "Ï"	Idiaeresis # LATIN CAPITAL LETTER I WITH DIAERESIS
<Multi_key> <I> <quotedbl>		: "Ï"	Idiaeresis # LATIN CAPITAL LETTER I WITH DIAERESIS
<Multi_key> <diaeresis> <I>		: "Ï"	Idiaeresis # LATIN CAPITAL LETTER I WITH DIAERESIS
<Multi_key> <I> <diaeresis>		: "Ï"	Idiaeresis # LATIN CAPITAL LETTER I WITH DIAERESIS
<dead_acute> <J>			: "J́"	# LATIN CAPITAL LETTER J plus COMBINING ACUTE
<Multi_key> <apostrophe> <J>		: "J́"	# LATIN CAPITAL LETTER J plus COMBINING ACUTE
<Multi_key> <J> <apostrophe>		: "J́"	# LATIN CAPITAL LETTER J plus COMBINING ACUTE
<Multi_key> <acute> <J>			: "J́"	# LATIN CAPITAL LETTER J plus COMBINING ACUTE
<Multi_key> <J> <acute>			: "J́"	# LATIN CAPITAL LETTER J plus COMBINING ACUTE
<Multi_key> <D> <H>			: "Ð"	ETH # LATIN CAPITAL LETTER ETH
<dead_tilde> <N>			: "Ñ"	Ntilde # LATIN CAPITAL LETTER N WITH TILDE
<Multi_key> <asciitilde> <N>		: "Ñ"	Ntilde # LATIN CAPITAL LETTER N WITH TILDE
<Multi_key> <N> <asciitilde>		: "Ñ"	Ntilde # LATIN CAPITAL LETTER N WITH TILDE
<dead_grave> <O>			: "Ò"	Ograve # LATIN CAPITAL LETTER O WITH GRAVE
<Multi_key> <grave> <O>			: "Ò"	Ograve # LATIN CAPITAL LETTER O WITH GRAVE
<Multi_key> <O> <grave>			: "Ò"	Ograve # LATIN CAPITAL LETTER O WITH GRAVE
<dead_acute> <O>			: "Ó"	Oacute # LATIN CAPITAL LETTER O WITH ACUTE
<Multi_key> <acute> <O>			: "Ó"	Oacute # LATIN CAPITAL LETTER O WITH ACUTE
<Multi_key> <O> <acute>			: "Ó"	Oacute # LATIN CAPITAL LETTER O WITH ACUTE
<Multi_key> <apostrophe> <O>		: "Ó"	Oacute # LATIN CAPITAL LETTER O WITH ACUTE
<Multi_key> <O> <apostrophe>		: "Ó"	Oacute # LATIN CAPITAL LETTER O WITH ACUTE
<dead_circumflex> <O>			: "Ô"	Ocircumflex # LATIN CAPITAL LETTER O WITH CIRCUMFLEX
<Multi_key> <asciicircum> <O>		: "Ô"	Ocircumflex # LATIN CAPITAL LETTER O WITH CIRCUMFLEX
<Multi_key> <O> <asciicircum>		: "Ô"	Ocircumflex # LATIN CAPITAL LETTER O WITH CIRCUMFLEX
<Multi_key> <greater> <O>		: "Ô"	Ocircumflex # LATIN CAPITAL LETTER O WITH CIRCUMFLEX
<Multi_key> <O> <greater>		: "Ô"	Ocircumflex # LATIN CAPITAL LETTER O WITH CIRCUMFLEX
<dead_tilde> <O>			: "Õ"	Otilde # LATIN CAPITAL LETTER O WITH TILDE
<Multi_key> <asciitilde> <O>		: "Õ"	Otilde # LATIN CAPITAL LETTER O WITH TILDE
<Multi_key> <O> <asciitilde>		: "Õ"	Otilde # LATIN CAPITAL LETTER O WITH TILDE
<dead_diaeresis> <O>			: "Ö"	Odiaeresis # LATIN CAPITAL LETTER O WITH DIAERESIS
<Multi_key> <quotedbl> <O>		: "Ö"	Odiaeresis # LATIN CAPITAL LETTER O WITH DIAERESIS
<Multi_key> <O> <quotedbl>		: "Ö"	Odiaeresis # LATIN CAPITAL LETTER O WITH DIAERESIS
<Multi_key> <diaeresis> <O>		: "Ö"	Odiaeresis # LATIN CAPITAL LETTER O WITH DIAERESIS
<Multi_key> <O> <diaeresis>		: "Ö"	Odiaeresis # LATIN CAPITAL LETTER O WITH DIAERESIS
<Multi_key> <x> <x>			: "×"	multiply # MULTIPLICATION SIGN
<dead_stroke> <O>			: "Ø"	Oslash # LATIN CAPITAL LETTER O WITH STROKE
<Multi_key> <slash> <O>			: "Ø"	Oslash # LATIN CAPITAL LETTER O WITH STROKE
<Multi_key> <O> <slash>			: "Ø"	Oslash # LATIN CAPITAL LETTER O WITH STROKE
<Multi_key> <KP_Divide> <O>		: "Ø"	Oslash # LATIN CAPITAL LETTER O WITH STROKE
<dead_grave> <U>			: "Ù"	Ugrave # LATIN CAPITAL LETTER U WITH GRAVE
<Multi_key> <grave> <U>			: "Ù"	Ugrave # LATIN CAPITAL LETTER U WITH GRAVE
<Multi_key> <U> <grave>			: "Ù"	Ugrave # LATIN CAPITAL LETTER U WITH GRAVE
<dead_acute> <U>			: "Ú"	Uacute # LATIN CAPITAL LETTER U WITH ACUTE
<Multi_key> <acute> <U>			: "Ú"	Uacute # LATIN CAPITAL LETTER U WITH ACUTE
<Multi_key> <U> <acute>			: "Ú"	Uacute # LATIN CAPITAL LETTER U WITH ACUTE
<Multi_key> <apostrophe> <U>		: "Ú"	Uacute # LATIN CAPITAL LETTER U WITH ACUTE
<Multi_key> <U> <apostrophe>		: "Ú"	Uacute # LATIN CAPITAL LETTER U WITH ACUTE
<dead_circumflex> <U>			: "Û"	Ucircumflex # LATIN CAPITAL LETTER U WITH CIRCUMFLEX
<Multi_key> <asciicircum> <U>		: "Û"	Ucircumflex # LATIN CAPITAL LETTER U WITH CIRCUMFLEX
<Multi_key> <U> <asciicircum>		: "Û"	Ucircumflex # LATIN CAPITAL LETTER U WITH CIRCUMFLEX
<Multi_key> <greater> <U>		: "Û"	Ucircumflex # LATIN CAPITAL LETTER U WITH CIRCUMFLEX
<Multi_key> <U> <greater>		: "Û"	Ucircumflex # LATIN CAPITAL LETTER U WITH CIRCUMFLEX
<dead_diaeresis> <U>			: "Ü"	Udiaeresis # LATIN CAPITAL LETTER U WITH DIAERESIS
<Multi_key> <quotedbl> <U>		: "Ü"	Udiaeresis # LATIN CAPITAL LETTER U WITH DIAERESIS
<Multi_key> <U> <quotedbl>		: "Ü"	Udiaeresis # LATIN CAPITAL LETTER U WITH DIAERESIS
<Multi_key> <diaeresis> <U>		: "Ü"	Udiaeresis # LATIN CAPITAL LETTER U WITH DIAERESIS
<Multi_key> <U> <diaeresis>		: "Ü"	Udiaeresis # LATIN CAPITAL LETTER U WITH DIAERESIS
<dead_acute> <Y>			: "Ý"	Yacute # LATIN CAPITAL LETTER Y WITH ACUTE
<Multi_key> <acute> <Y>			: "Ý"	Yacute # LATIN CAPITAL LETTER Y WITH ACUTE
<Multi_key> <Y> <acute>			: "Ý"	Yacute # LATIN CAPITAL LETTER Y WITH ACUTE
<Multi_key> <apostrophe> <Y>		: "Ý"	Yacute # LATIN CAPITAL LETTER Y WITH ACUTE
<Multi_key> <Y> <apostrophe>		: "Ý"	Yacute # LATIN CAPITAL LETTER Y WITH ACUTE
<Multi_key> <T> <H>			: "Þ"	THORN # LATIN CAPITAL LETTER THORN
<dead_grave> <a>			: "à"	agrave # LATIN SMALL LETTER A WITH GRAVE
<Multi_key> <grave> <a>			: "à"	agrave # LATIN SMALL LETTER A WITH GRAVE
<Multi_key> <a> <grave>			: "à"	agrave # LATIN SMALL LETTER A WITH GRAVE
<dead_acute> <a>			: "á"	aacute # LATIN SMALL LETTER A WITH ACUTE
<Multi_key> <acute> <a>			: "á"	aacute # LATIN SMALL LETTER A WITH ACUTE
<Multi_key> <a> <acute>			: "á"	aacute # LATIN SMALL LETTER A WITH ACUTE
<Multi_key> <apostrophe> <a>		: "á"	aacute # LATIN SMALL LETTER A WITH ACUTE
<Multi_key> <a> <apostrophe>		: "á"	aacute # LATIN SMALL LETTER A WITH ACUTE
<dead_circumflex> <a>			: "â"	acircumflex # LATIN SMALL LETTER A WITH CIRCUMFLEX
<Multi_key> <asciicircum> <a>		: "â"	acircumflex # LATIN SMALL LETTER A WITH CIRCUMFLEX
<Multi_key> <a> <asciicircum>		: "â"	acircumflex # LATIN SMALL LETTER A WITH CIRCUMFLEX
<Multi_key> <greater> <a>		: "â"	acircumflex # LATIN SMALL LETTER A WITH CIRCUMFLEX
<Multi_key> <a> <greater>		: "â"	acircumflex # LATIN SMALL LETTER A WITH CIRCUMFLEX
<dead_tilde> <a>			: "ã"	atilde # LATIN SMALL LETTER A WITH TILDE
<Multi_key> <asciitilde> <a>		: "ã"	atilde # LATIN SMALL LETTER A WITH TILDE
<Multi_key> <a> <asciitilde>		: "ã"	atilde # LATIN SMALL LETTER A WITH TILDE
<dead_diaeresis> <a>			: "ä"	adiaeresis # LATIN SMALL LETTER A WITH DIAERESIS
<Multi_key> <quotedbl> <a>		: "ä"	adiaeresis # LATIN SMALL LETTER A WITH DIAERESIS
<Multi_key> <a> <quotedbl>		: "ä"	adiaeresis # LATIN SMALL LETTER A WITH DIAERESIS
<Multi_key> <diaeresis> <a>		: "ä"	adiaeresis # LATIN SMALL LETTER A WITH DIAERESIS
<Multi_key> <a> <diaeresis>		: "ä"	adiaeresis # LATIN SMALL LETTER A WITH DIAERESIS
<dead_abovering> <a>			: "å"	aring # LATIN SMALL LETTER A WITH RING ABOVE
<Multi_key> <o> <a>			: "å"	aring # LATIN SMALL LETTER A WITH RING ABOVE
<Multi_key> <asterisk> <a>		: "å"	aring # LATIN SMALL LETTER A WITH RING ABOVE
<Multi_key> <a> <asterisk>		: "å"	aring # LATIN SMALL LETTER A WITH RING ABOVE
<Multi_key> <a> <a>			: "å"	aring # LATIN SMALL LETTER A WITH RING ABOVE
<dead_cedilla> <c>			: "ç"	ccedilla # LATIN SMALL LETTER C WITH CEDILLA
<Multi_key> <comma> <c>			: "ç"	ccedilla # LATIN SMALL LETTER C WITH CEDILLA
<Multi_key> <c> <comma>			: "ç"	ccedilla # LATIN SMALL LETTER C WITH CEDILLA
<Multi_key> <cedilla> <c>		: "ç"	ccedilla # LATIN SMALL LETTER C WITH CEDILLA
<dead_grave> <e>			: "è"	egrave # LATIN SMALL LETTER E WITH GRAVE
<Multi_key> <grave> <e>			: "è"	egrave # LATIN SMALL LETTER E WITH GRAVE
<Multi_key> <e> <grave>			: "è"	egrave # LATIN SMALL LETTER E WITH GRAVE
<dead_acute> <e>			: "é"	eacute # LATIN SMALL LETTER E WITH ACUTE
<Multi_key> <acute> <e>			: "é"	eacute # LATIN SMALL LETTER E WITH ACUTE
<Multi_key> <e> <acute>			: "é"	eacute # LATIN SMALL LETTER E WITH ACUTE
<Multi_key> <apostrophe> <e>		: "é"	eacute # LATIN SMALL LETTER E WITH ACUTE
<Multi_key> <e> <apostrophe>		: "é"	eacute # LATIN SMALL LETTER E WITH ACUTE
<dead_circumflex> <e>			: "ê"	ecircumflex # LATIN SMALL LETTER E WITH CIRCUMFLEX
<Multi_key> <asciicircum> <e>		: "ê"	ecircumflex # LATIN SMALL LETTER E WITH CIRCUMFLEX
<Multi_key> <e> <asciicircum>		: "ê"	ecircumflex # LATIN SMALL LETTER E WITH CIRCUMFLEX
<Multi_key> <greater> <e>		: "ê"	ecircumflex # LATIN SMALL LETTER E WITH CIRCUMFLEX
<Multi_key> <e> <greater>		: "ê"	ecircumflex # LATIN SMALL LETTER E WITH CIRCUMFLEX
<dead_diaeresis> <e>			: "ë"	ediaeresis # LATIN SMALL LETTER E WITH DIAERESIS
<Multi_key> <quotedbl> <e>		: "ë"	ediaeresis # LATIN SMALL LETTER E WITH DIAERESIS
<Multi_key> <e> <quotedbl>		: "ë"	ediaeresis # LATIN SMALL LETTER E WITH DIAERESIS
<Multi_key> <diaeresis> <e>		: "ë"	ediaeresis # LATIN SMALL LETTER E WITH DIAERESIS
<Multi_key> <e> <diaeresis>		: "ë"	ediaeresis # LATIN SMALL LETTER E WITH DIAERESIS
<dead_grave> <i>			: "ì"	igrave # LATIN SMALL LETTER I WITH GRAVE
<Multi_key> <grave> <i>			: "ì"	igrave # LATIN SMALL LETTER I WITH GRAVE
<Multi_key> <i> <grave>			: "ì"	igrave # LATIN SMALL LETTER I WITH GRAVE
<dead_acute> <i>			: "í"	iacute # LATIN SMALL LETTER I WITH ACUTE
<Multi_key> <acute> <i>			: "í"	iacute # LATIN SMALL LETTER I WITH ACUTE
<Multi_key> <i> <acute>			: "í"	iacute # LATIN SMALL LETTER I WITH ACUTE
<Multi_key> <apostrophe> <i>		: "í"	iacute # LATIN SMALL LETTER I WITH ACUTE
<Multi_key> <i> <apostrophe>		: "í"	iacute # LATIN SMALL LETTER I WITH ACUTE
<dead_circumflex> <i>			: "î"	icircumflex # LATIN SMALL LETTER I WITH CIRCUMFLEX
<Multi_key> <asciicircum> <i>		: "î"	icircumflex # LATIN SMALL LETTER I WITH CIRCUMFLEX
<Multi_key> <i> <asciicircum>		: "î"	icircumflex # LATIN SMALL LETTER I WITH CIRCUMFLEX
<Multi_key> <greater> <i>		: "î"	icircumflex # LATIN SMALL LETTER I WITH CIRCUMFLEX
<Multi_key> <i> <greater>		: "î"	icircumflex # LATIN SMALL LETTER I WITH CIRCUMFLEX
<dead_diaeresis> <i>			: "ï"	idiaeresis # LATIN SMALL LETTER I WITH DIAERESIS
<Multi_key> <quotedbl> <i>		: "ï"	idiaeresis # LATIN SMALL LETTER I WITH DIAERESIS
<Multi_key> <i> <quotedbl>		: "ï"	idiaeresis # LATIN SMALL LETTER I WITH DIAERESIS
<Multi_key> <diaeresis> <i>		: "ï"	idiaeresis # LATIN SMALL LETTER I WITH DIAERESIS
<Multi_key> <i> <diaeresis>		: "ï"	idiaeresis # LATIN SMALL LETTER I WITH DIAERESIS
<dead_acute> <j>			: "j́"	# LATIN SMALL LETTER J plus COMBINING ACUTE
<Multi_key> <apostrophe> <j>		: "j́"	# LATIN SMALL LETTER J plus COMBINING ACUTE
<Multi_key> <j> <apostrophe>		: "j́"	# LATIN SMALL LETTER J plus COMBINING ACUTE
<Multi_key> <acute> <j>			: "j́"	# LATIN SMALL LETTER J plus COMBINING ACUTE
<Multi_key> <j> <acute>			: "j́"	# LATIN SMALL LETTER J plus COMBINING ACUTE
<Multi_key> <d> <h>			: "ð"	eth # LATIN SMALL LETTER ETH
<dead_tilde> <n>			: "ñ"	ntilde # LATIN SMALL LETTER N WITH TILDE
<Multi_key> <asciitilde> <n>		: "ñ"	ntilde # LATIN SMALL LETTER N WITH TILDE
<Multi_key> <n> <asciitilde>		: "ñ"	ntilde # LATIN SMALL LETTER N WITH TILDE
<dead_grave> <o>			: "ò"	ograve # LATIN SMALL LETTER O WITH GRAVE
<Multi_key> <grave> <o>			: "ò"	ograve # LATIN SMALL LETTER O WITH GRAVE
<Multi_key> <o> <grave>			: "ò"	ograve # LATIN SMALL LETTER O WITH GRAVE
<dead_acute> <o>			: "ó"	oacute # LATIN SMALL LETTER O WITH ACUTE
<Multi_key> <acute> <o>			: "ó"	oacute # LATIN SMALL LETTER O WITH ACUTE
<Multi_key> <o> <acute>			: "ó"	oacute # LATIN SMALL LETTER O WITH ACUTE
<Multi_key> <apostrophe> <o>		: "ó"	oacute # LATIN SMALL LETTER O WITH ACUTE
<Multi_key> <o> <apostrophe>		: "ó"	oacute # LATIN SMALL LETTER O WITH ACUTE
<dead_circumflex> <o>			: "ô"	ocircumflex # LATIN SMALL LETTER O WITH CIRCUMFLEX
<Multi_key> <asciicircum> <o>		: "ô"	ocircumflex # LATIN SMALL LETTER O WITH CIRCUMFLEX
<Multi_key> <o> <asciicircum>		: "ô"	ocircumflex # LATIN SMALL LETTER O WITH CIRCUMFLEX
<Multi_key> <greater> <o>		: "ô"	ocircumflex # LATIN SMALL LETTER O WITH CIRCUMFLEX
<Multi_key> <o> <greater>		: "ô"	ocircumflex # LATIN SMALL LETTER O WITH CIRCUMFLEX
<dead_tilde> <o>			: "õ"	otilde # LATIN SMALL LETTER O WITH TILDE
<Multi_key> <asciitilde> <o>		: "õ"	otilde # LATIN SMALL LETTER O WITH TILDE
<Multi_key> <o> <asciitilde>		: "õ"	otilde # LATIN SMALL LETTER O WITH TILDE
<dead_diaeresis> <o>			: "ö"	odiaeresis # LATIN SMALL LETTER O WITH DIAERESIS
<Multi_key> <o> <diaeresis>		: "ö"	odiaeresis # LATIN SMALL LETTER O WITH DIAERESIS
<Multi_key> <diaeresis> <o>		: "ö"	odiaeresis # LATIN SMALL LETTER O WITH DIAERESIS
<Multi_key> <quotedbl> <o>		: "ö"	odiaeresis # LATIN SMALL LETTER O WITH DIAERESIS
<Multi_key> <o> <quotedbl>		: "ö"	odiaeresis # LATIN SMALL LETTER O WITH DIAERESIS
<Multi_key> <colon> <minus>		: "÷"	division # DIVISION SIGN
<Multi_key> <minus> <colon>		: "÷"	division # DIVISION SIGN
<dead_stroke> <o>			: "ø"	oslash # LATIN SMALL LETTER O WITH STROKE
<Multi_key> <slash> <o>			: "ø"	oslash # LATIN SMALL LETTER O WITH STROKE
<Multi_key> <o> <slash>			: "ø"	oslash # LATIN SMALL LETTER O WITH STROKE
<Multi_key> <KP_Divide> <o>		: "ø"	oslash # LATIN SMALL LETTER O WITH STROKE
<dead_grave> <u>			: "ù"	ugrave # LATIN SMALL LETTER U WITH GRAVE
<Multi_key> <grave> <u>			: "ù"	ugrave # LATIN SMALL LETTER U WITH GRAVE
<Multi_key> <u> <grave>			: "ù"	ugrave # LATIN SMALL LETTER U WITH GRAVE
<dead_acute> <u>			: "ú"	uacute # LATIN SMALL LETTER U WITH ACUTE
<Multi_key> <acute> <u>			: "ú"	uacute # LATIN SMALL LETTER U WITH ACUTE
<Multi_key> <u> <acute>			: "ú"	uacute # LATIN SMALL LETTER U WITH ACUTE
<Multi_key> <apostrophe> <u>		: "ú"	uacute # LATIN SMALL LETTER U WITH ACUTE
<Multi_key> <u> <apostrophe>		: "ú"	uacute # LATIN SMALL LETTER U WITH ACUTE
<dead_circumflex> <u>			: "û"	ucircumflex # LATIN SMALL LETTER U WITH CIRCUMFLEX
<Multi_key> <asciicircum> <u>		: "û"	ucircumflex # LATIN SMALL LETTER U WITH CIRCUMFLEX
<Multi_key> <u> <asciicircum>		: "û"	ucircumflex # LATIN SMALL LETTER U WITH CIRCUMFLEX
<Multi_key> <greater> <u>		: "û"	ucircumflex # LATIN SMALL LETTER U WITH CIRCUMFLEX
<Multi_key> <u> <greater>		: "û"	ucircumflex # LATIN SMALL LETTER U WITH CIRCUMFLEX
<dead_diaeresis> <u>			: "ü"	udiaeresis # LATIN SMALL LETTER U WITH DIAERESIS
<Multi_key> <quotedbl> <u>		: "ü"	udiaeresis # LATIN SMALL LETTER U WITH DIAERESIS
<Multi_key> <u> <quotedbl>		: "ü"	udiaeresis # LATIN SMALL LETTER U WITH DIAERESIS
<Multi_key> <diaeresis> <u>		: "ü"	udiaeresis # LATIN SMALL LETTER U WITH DIAERESIS
<Multi_key> <u> <diaeresis>		: "ü"	udiaeresis # LATIN SMALL LETTER U WITH DIAERESIS
<dead_acute> <y>			: "ý"	yacute # LATIN SMALL LETTER Y WITH ACUTE
<Multi_key> <acute> <y>			: "ý"	yacute # LATIN SMALL LETTER Y WITH ACUTE
<Multi_key> <y> <acute>			: "ý"	yacute # LATIN SMALL LETTER Y WITH ACUTE
<Multi_key> <apostrophe> <y>		: "ý"	yacute # LATIN SMALL LETTER Y WITH ACUTE
<Multi_key> <y> <apostrophe>		: "ý"	yacute # LATIN SMALL LETTER Y WITH ACUTE
<Multi_key> <t> <h>			: "þ"	thorn # LATIN SMALL LETTER THORN
<dead_diaeresis> <y>			: "ÿ"	ydiaeresis # LATIN SMALL LETTER Y WITH DIAERESIS
<Multi_key> <quotedbl> <y>		: "ÿ"	ydiaeresis # LATIN SMALL LETTER Y WITH DIAERESIS
<Multi_key> <y> <quotedbl>		: "ÿ"	ydiaeresis # LATIN SMALL LETTER Y WITH DIAERESIS
<Multi_key> <diaeresis> <y>		: "ÿ"	ydiaeresis # LATIN SMALL LETTER Y WITH DIAERESIS
<Multi_key> <y> <diaeresis>		: "ÿ"	ydiaeresis # LATIN SMALL LETTER Y WITH DIAERESIS
# Latin Extended-A
<dead_macron> <A>			: "Ā"	U0100 # LATIN CAPITAL LETTER A WITH MACRON
<Multi_key> <macron> <A>		: "Ā"	U0100 # LATIN CAPITAL LETTER A WITH MACRON
<Multi_key> <underscore> <A>		: "Ā"	U0100 # LATIN CAPITAL LETTER A WITH MACRON
<Multi_key> <A> <underscore>		: "Ā"	U0100 # LATIN CAPITAL LETTER A WITH MACRON
<Multi_key> <minus> <A>			: "Ā"	U0100 # LATIN CAPITAL LETTER A WITH MACRON
<Multi_key> <A> <minus>			: "Ā"	U0100 # LATIN CAPITAL LETTER A WITH MACRON
<dead_macron> <a>			: "ā"	U0101 # LATIN SMALL LETTER A WITH MACRON
<Multi_key> <macron> <a>		: "ā"	U0101 # LATIN SMALL LETTER A WITH MACRON
<Multi_key> <underscore> <a>		: "ā"	U0101 # LATIN SMALL LETTER A WITH MACRON
<Multi_key> <a> <underscore>		: "ā"	U0101 # LATIN SMALL LETTER A WITH MACRON
<Multi_key> <minus> <a>			: "ā"	U0101 # LATIN SMALL LETTER A WITH MACRON
<Multi_key> <a> <minus>			: "ā"	U0101 # LATIN SMALL LETTER A WITH MACRON
<dead_breve> <A>			: "Ă"	U0102 # LATIN CAPITAL LETTER A WITH BREVE
<Multi_key> <U> <A>			: "Ă"	U0102 # LATIN CAPITAL LETTER A WITH BREVE
<Multi_key> <u> <A>			: "Ă"	U0102 # LATIN CAPITAL LETTER A WITH BREVE
<Multi_key> <b> <A>			: "Ă"	U0102 # LATIN CAPITAL LETTER A WITH BREVE
<Multi_key> <A> <parenleft>		: "Ă"	U0102 # LATIN CAPITAL LETTER A WITH BREVE
<dead_breve> <a>			: "ă"	U0103 # LATIN SMALL LETTER A WITH BREVE
<Multi_key> <U> <a>			: "ă"	U0103 # LATIN SMALL LETTER A WITH BREVE
<Multi_key> <u> <a>			: "ă"	U0103 # LATIN SMALL LETTER A WITH BREVE
<Multi_key> <b> <a>			: "ă"	U0103 # LATIN SMALL LETTER A WITH BREVE
<Multi_key> <a> <parenleft>		: "ă"	U0103 # LATIN SMALL LETTER A WITH BREVE
<dead_ogonek> <A>			: "Ą"	U0104 # LATIN CAPITAL LETTER A WITH OGONEK
<Multi_key> <semicolon> <A>		: "Ą"	U0104 # LATIN CAPITAL LETTER A WITH OGONEK
<Multi_key> <A> <semicolon>		: "Ą"	U0104 # LATIN CAPITAL LETTER A WITH OGONEK
<Multi_key> <comma> <A>			: "Ą"	U0104 # LATIN CAPITAL LETTER A WITH OGONEK
<Multi_key> <A> <comma>			: "Ą"	U0104 # LATIN CAPITAL LETTER A WITH OGONEK
<dead_ogonek> <a>			: "ą"	U0105 # LATIN SMALL LETTER A WITH OGONEK
<Multi_key> <semicolon> <a>		: "ą"	U0105 # LATIN SMALL LETTER A WITH OGONEK
<Multi_key> <a> <semicolon>		: "ą"	U0105 # LATIN SMALL LETTER A WITH OGONEK
<Multi_key> <comma> <a>			: "ą"	U0105 # LATIN SMALL LETTER A WITH OGONEK
<Multi_key> <a> <comma>			: "ą"	U0105 # LATIN SMALL LETTER A WITH OGONEK
<dead_acute> <C>			: "Ć"	U0106 # LATIN CAPITAL LETTER C WITH ACUTE
<Multi_key> <acute> <C>			: "Ć"	U0106 # LATIN CAPITAL LETTER C WITH ACUTE
<Multi_key> <apostrophe> <C>		: "Ć"	U0106 # LATIN CAPITAL LETTER C WITH ACUTE
<Multi_key> <C> <apostrophe>		: "Ć"	U0106 # LATIN CAPITAL LETTER C WITH ACUTE
<dead_acute> <c>			: "ć"	U0107 # LATIN SMALL LETTER C WITH ACUTE
<Multi_key> <acute> <c>			: "ć"	U0107 # LATIN SMALL LETTER C WITH ACUTE
<Multi_key> <apostrophe> <c>		: "ć"	U0107 # LATIN SMALL LETTER C WITH ACUTE
<Multi_key> <c> <apostrophe>		: "ć"	U0107 # LATIN SMALL LETTER C WITH ACUTE
<dead_circumflex> <C>			: "Ĉ"	U0108 # LATIN CAPITAL LETTER C WITH CIRCUMFLEX
<Multi_key> <asciicircum> <C>		: "Ĉ"	U0108 # LATIN CAPITAL LETTER C WITH CIRCUMFLEX
<dead_circumflex> <c>			: "ĉ"	U0109 # LATIN SMALL LETTER C WITH CIRCUMFLEX
<Multi_key> <asciicircum> <c>		: "ĉ"	U0109 # LATIN SMALL LETTER C WITH CIRCUMFLEX
<dead_abovedot> <C>			: "Ċ"	U010A # LATIN CAPITAL LETTER C WITH DOT ABOVE
<Multi_key> <period> <C>		: "Ċ"	U010A # LATIN CAPITAL LETTER C WITH DOT ABOVE
<Multi_key> <C> <period>		: "Ċ"	U010A # LATIN CAPITAL LETTER C WITH DOT ABOVE
<dead_abovedot> <c>			: "ċ"	U010B # LATIN SMALL LETTER C WITH DOT ABOVE
<Multi_key> <period> <c>		: "ċ"	U010B # LATIN SMALL LETTER C WITH DOT ABOVE
<Multi_key> <c> <period>		: "ċ"	U010B # LATIN SMALL LETTER C WITH DOT ABOVE
<dead_caron> <C>			: "Č"	U010C # LATIN CAPITAL LETTER C WITH CARON
<Multi_key> <c> <C>			: "Č"	U010C # LATIN CAPITAL LETTER C WITH CARON
<Multi_key> <v> <C>			: "Č"	U010C # LATIN CAPITAL LETTER C WITH CARON
<Multi_key> <less> <C>			: "Č"	U010C # LATIN CAPITAL LETTER C WITH CARON
<Multi_key> <C> <less>			: "Č"	U010C # LATIN CAPITAL LETTER C WITH CARON
<dead_caron> <c>			: "č"	U010D # LATIN SMALL LETTER C WITH CARON
<Multi_key> <c> <c>			: "č"	U010D # LATIN SMALL LETTER C WITH CARON
<Multi_key> <v> <c>			: "č"	U010D # LATIN SMALL LETTER C WITH CARON
<Multi_key> <less> <c>			: "č"	U010D # LATIN SMALL LETTER C WITH CARON
<Multi_key> <c> <less>			: "č"	U010D # LATIN SMALL LETTER C WITH CARON
<dead_caron> <D>			: "Ď"	U010E # LATIN CAPITAL LETTER D WITH CARON
<Multi_key> <c> <D>			: "Ď"	U010E # LATIN CAPITAL LETTER D WITH CARON
<Multi_key> <v> <D>			: "Ď"	U010E # LATIN CAPITAL LETTER D WITH CARON
<Multi_key> <less> <D>			: "Ď"	U010E # LATIN CAPITAL LETTER D WITH CARON
<Multi_key> <D> <less>			: "Ď"	U010E # LATIN CAPITAL LETTER D WITH CARON
<dead_caron> <d>			: "ď"	U010F # LATIN SMALL LETTER D WITH CARON
<Multi_key> <c> <d>			: "ď"	U010F # LATIN SMALL LETTER D WITH CARON
<Multi_key> <v> <d>			: "ď"	U010F # LATIN SMALL LETTER D WITH CARON
<Multi_key> <less> <d>			: "ď"	U010F # LATIN SMALL LETTER D WITH CARON
<Multi_key> <d> <less>			: "ď"	U010F # LATIN SMALL LETTER D WITH CARON
<dead_stroke> <D>			: "Đ"	Dstroke # LATIN CAPITAL LETTER D WITH STROKE
<Multi_key> <minus> <D>			: "Đ"	Dstroke # LATIN CAPITAL LETTER D WITH STROKE
<Multi_key> <D> <minus>			: "Đ"	Dstroke # LATIN CAPITAL LETTER D WITH STROKE
<Multi_key> <slash> <D>			: "Đ"	Dstroke # LATIN CAPITAL LETTER D WITH STROKE
<Multi_key> <KP_Divide> <D>		: "Đ"	Dstroke # LATIN CAPITAL LETTER D WITH STROKE
<dead_stroke> <d>			: "đ"	dstroke # LATIN SMALL LETTER D WITH STROKE
<Multi_key> <minus> <d>			: "đ"	dstroke # LATIN SMALL LETTER D WITH STROKE
<Multi_key> <d> <minus>			: "đ"	dstroke # LATIN SMALL LETTER D WITH STROKE
<Multi_key> <slash> <d>			: "đ"	dstroke # LATIN SMALL LETTER D WITH STROKE
<Multi_key> <KP_Divide> <d>		: "đ"	dstroke # LATIN SMALL LETTER D WITH STROKE
<dead_macron> <E>			: "Ē"	U0112 # LATIN CAPITAL LETTER E WITH MACRON
<Multi_key> <macron> <E>		: "Ē"	U0112 # LATIN CAPITAL LETTER E WITH MACRON
<Multi_key> <underscore> <E>		: "Ē"	U0112 # LATIN CAPITAL LETTER E WITH MACRON
<Multi_key> <E> <underscore>		: "Ē"	U0112 # LATIN CAPITAL LETTER E WITH MACRON
<Multi_key> <minus> <E>			: "Ē"	U0112 # LATIN CAPITAL LETTER E WITH MACRON
<Multi_key> <E> <minus>			: "Ē"	U0112 # LATIN CAPITAL LETTER E WITH MACRON
<dead_macron> <e>			: "ē"	U0113 # LATIN SMALL LETTER E WITH MACRON
<Multi_key> <macron> <e>		: "ē"	U0113 # LATIN SMALL LETTER E WITH MACRON
<Multi_key> <underscore> <e>		: "ē"	U0113 # LATIN SMALL LETTER E WITH MACRON
<Multi_key> <e> <underscore>		: "ē"	U0113 # LATIN SMALL LETTER E WITH MACRON
<Multi_key> <minus> <e>			: "ē"	U0113 # LATIN SMALL LETTER E WITH MACRON
<Multi_key> <e> <minus>			: "ē"	U0113 # LATIN SMALL LETTER E WITH MACRON
<dead_breve> <E>			: "Ĕ"	U0114 # LATIN CAPITAL LETTER E WITH BREVE
<Multi_key> <U> <E>			: "Ĕ"	U0114 # LATIN CAPITAL LETTER E WITH BREVE
<Multi_key> <u> <E>			: "Ĕ"	U0114 # LATIN CAPITAL LETTER E WITH BREVE
<Multi_key> <b> <E>			: "Ĕ"	U0114 # LATIN CAPITAL LETTER E WITH BREVE
<dead_breve> <e>			: "ĕ"	U0115 # LATIN SMALL LETTER E WITH BREVE
<Multi_key> <U> <e>			: "ĕ"	U0115 # LATIN SMALL LETTER E WITH BREVE
<Multi_key> <u> <e>			: "ĕ"	U0115 # LATIN SMALL LETTER E WITH BREVE
<Multi_key> <b> <e>			: "ĕ"	U0115 # LATIN SMALL LETTER E WITH BREVE
<dead_abovedot> <E>			: "Ė"	U0116 # LATIN CAPITAL LETTER E WITH DOT ABOVE
<Multi_key> <period> <E>		: "Ė"	U0116 # LATIN CAPITAL LETTER E WITH DOT ABOVE
<Multi_key> <E> <period>		: "Ė"	U0116 # LATIN CAPITAL LETTER E WITH DOT ABOVE
<dead_abovedot> <e>			: "ė"	U0117 # LATIN SMALL LETTER E WITH DOT ABOVE
<Multi_key> <period> <e>		: "ė"	U0117 # LATIN SMALL LETTER E WITH DOT ABOVE
<Multi_key> <e> <period>		: "ė"	U0117 # LATIN SMALL LETTER E WITH DOT ABOVE
<dead_ogonek> <E>			: "Ę"	U0118 # LATIN CAPITAL LETTER E WITH OGONEK
<Multi_key> <semicolon> <E>		: "Ę"	U0118 # LATIN CAPITAL LETTER E WITH OGONEK
<Multi_key> <E> <semicolon>		: "Ę"	U0118 # LATIN CAPITAL LETTER E WITH OGONEK
<Multi_key> <comma> <E>			: "Ę"	U0118 # LATIN CAPITAL LETTER E WITH OGONEK
<Multi_key> <E> <comma>			: "Ę"	U0118 # LATIN CAPITAL LETTER E WITH OGONEK
<dead_ogonek> <e>			: "ę"	U0119 # LATIN SMALL LETTER E WITH OGONEK
<Multi_key> <semicolon> <e>		: "ę"	U0119 # LATIN SMALL LETTER E WITH OGONEK
<Multi_key> <e> <semicolon>		: "ę"	U0119 # LATIN SMALL LETTER E WITH OGONEK
<Multi_key> <comma> <e>			: "ę"	U0119 # LATIN SMALL LETTER E WITH OGONEK
<Multi_key> <e> <comma>			: "ę"	U0119 # LATIN SMALL LETTER E WITH OGONEK
<dead_caron> <E>			: "Ě"	U011A # LATIN CAPITAL LETTER E WITH CARON
<Multi_key> <c> <E>			: "Ě"	U011A # LATIN CAPITAL LETTER E WITH CARON
<Multi_key> <v> <E>			: "Ě"	U011A # LATIN CAPITAL LETTER E WITH CARON
<Multi_key> <less> <E>			: "Ě"	U011A # LATIN CAPITAL LETTER E WITH CARON
<Multi_key> <E> <less>			: "Ě"	U011A # LATIN CAPITAL LETTER E WITH CARON
<dead_caron> <e>			: "ě"	U011B # LATIN SMALL LETTER E WITH CARON
<Multi_key> <c> <e>			: "ě"	U011B # LATIN SMALL LETTER E WITH CARON
<Multi_key> <v> <e>			: "ě"	U011B # LATIN SMALL LETTER E WITH CARON
<Multi_key> <less> <e>			: "ě"	U011B # LATIN SMALL LETTER E WITH CARON
<Multi_key> <e> <less>			: "ě"	U011B # LATIN SMALL LETTER E WITH CARON
<dead_circumflex> <G>			: "Ĝ"	U011C # LATIN CAPITAL LETTER G WITH CIRCUMFLEX
<Multi_key> <asciicircum> <G>		: "Ĝ"	U011C # LATIN CAPITAL LETTER G WITH CIRCUMFLEX
<dead_circumflex> <g>			: "ĝ"	U011D # LATIN SMALL LETTER G WITH CIRCUMFLEX
<Multi_key> <asciicircum> <g>		: "ĝ"	U011D # LATIN SMALL LETTER G WITH CIRCUMFLEX
<dead_breve> <G>			: "Ğ"	U011E # LATIN CAPITAL LETTER G WITH BREVE
<Multi_key> <U> <G>			: "Ğ"	U011E # LATIN CAPITAL LETTER G WITH BREVE
<Multi_key> <u> <G>			: "Ğ"	U011E # LATIN CAPITAL LETTER G WITH BREVE
<Multi_key> <b> <G>			: "Ğ"	U011E # LATIN CAPITAL LETTER G WITH BREVE
<Multi_key> <breve> <G>			: "Ğ"	U011E # LATIN CAPITAL LETTER G WITH BREVE
<Multi_key> <G> <breve>			: "Ğ"	U011E # LATIN CAPITAL LETTER G WITH BREVE
<Multi_key> <G> <U>			: "Ğ"	U011E # LATIN CAPITAL LETTER G WITH BREVE
<Multi_key> <G> <parenleft>		: "Ğ"	U011E # LATIN CAPITAL LETTER G WITH BREVE
<dead_breve> <g>			: "ğ"	U011F # LATIN SMALL LETTER G WITH BREVE
<Multi_key> <U> <g>			: "ğ"	U011F # LATIN SMALL LETTER G WITH BREVE
<Multi_key> <u> <g>			: "ğ"	U011F # LATIN SMALL LETTER G WITH BREVE
<Multi_key> <b> <g>			: "ğ"	U011F # LATIN SMALL LETTER G WITH BREVE
<Multi_key> <breve> <g>			: "ğ"	U011F # LATIN SMALL LETTER G WITH BREVE
<Multi_key> <g> <breve>			: "ğ"	U011F # LATIN SMALL LETTER G WITH BREVE
<Multi_key> <g> <U>			: "ğ"	U011F # LATIN SMALL LETTER G WITH BREVE
<Multi_key> <g> <parenleft>		: "ğ"	U011F # LATIN SMALL LETTER G WITH BREVE
<dead_abovedot> <G>			: "Ġ"	U0120 # LATIN CAPITAL LETTER G WITH DOT ABOVE
<Multi_key> <period> <G>		: "Ġ"	U0120 # LATIN CAPITAL LETTER G WITH DOT ABOVE
<Multi_key> <G> <period>		: "Ġ"	U0120 # LATIN CAPITAL LETTER G WITH DOT ABOVE
<dead_abovedot> <g>			: "ġ"	U0121 # LATIN SMALL LETTER G WITH DOT ABOVE
<Multi_key> <period> <g>		: "ġ"	U0121 # LATIN SMALL LETTER G WITH DOT ABOVE
<Multi_key> <g> <period>		: "ġ"	U0121 # LATIN SMALL LETTER G WITH DOT ABOVE
<dead_cedilla> <G>			: "Ģ"	U0122 # LATIN CAPITAL LETTER G WITH CEDILLA
<Multi_key> <comma> <G>			: "Ģ"	U0122 # LATIN CAPITAL LETTER G WITH CEDILLA
<Multi_key> <G> <comma>			: "Ģ"	U0122 # LATIN CAPITAL LETTER G WITH CEDILLA
<Multi_key> <cedilla> <G>		: "Ģ"	U0122 # LATIN CAPITAL LETTER G WITH CEDILLA
<dead_cedilla> <g>			: "ģ"	U0123 # LATIN SMALL LETTER G WITH CEDILLA
<Multi_key> <comma> <g>			: "ģ"	U0123 # LATIN SMALL LETTER G WITH CEDILLA
<Multi_key> <g> <comma>			: "ģ"	U0123 # LATIN SMALL LETTER G WITH CEDILLA
<Multi_key> <cedilla> <g>		: "ģ"	U0123 # LATIN SMALL LETTER G WITH CEDILLA
<dead_circumflex> <H>			: "Ĥ"	U0124 # LATIN CAPITAL LETTER H WITH CIRCUMFLEX
<Multi_key> <asciicircum> <H>		: "Ĥ"	U0124 # LATIN CAPITAL LETTER H WITH CIRCUMFLEX
<dead_circumflex> <h>			: "ĥ"	U0125 # LATIN SMALL LETTER H WITH CIRCUMFLEX
<Multi_key> <asciicircum> <h>		: "ĥ"	U0125 # LATIN SMALL LETTER H WITH CIRCUMFLEX
<dead_stroke> <H>			: "Ħ"	U0126 # LATIN CAPITAL LETTER H WITH STROKE
<Multi_key> <slash> <H>			: "Ħ"	U0126 # LATIN CAPITAL LETTER H WITH STROKE
<Multi_key> <KP_Divide> <H>		: "Ħ"	U0126 # LATIN CAPITAL LETTER H WITH STROKE
<dead_stroke> <h>			: "ħ"	U0127 # LATIN SMALL LETTER H WITH STROKE
<Multi_key> <slash> <h>			: "ħ"	U0127 # LATIN SMALL LETTER H WITH STROKE
<Multi_key> <KP_Divide> <h>		: "ħ"	U0127 # LATIN SMALL LETTER H WITH STROKE
<dead_tilde> <I>			: "Ĩ"	U0128 # LATIN CAPITAL LETTER I WITH TILDE
<Multi_key> <asciitilde> <I>		: "Ĩ"	U0128 # LATIN CAPITAL LETTER I WITH TILDE
<Multi_key> <I> <asciitilde>		: "Ĩ"	U0128 # LATIN CAPITAL LETTER I WITH TILDE
<dead_tilde> <i>			: "ĩ"	U0129 # LATIN SMALL LETTER I WITH TILDE
<Multi_key> <asciitilde> <i>		: "ĩ"	U0129 # LATIN SMALL LETTER I WITH TILDE
<Multi_key> <i> <asciitilde>		: "ĩ"	U0129 # LATIN SMALL LETTER I WITH TILDE
<dead_macron> <I>			: "Ī"	U012A # LATIN CAPITAL LETTER I WITH MACRON
<Multi_key> <macron> <I>		: "Ī"	U012A # LATIN CAPITAL LETTER I WITH MACRON
<Multi_key> <underscore> <I>		: "Ī"	U012A # LATIN CAPITAL LETTER I WITH MACRON
<Multi_key> <I> <underscore>		: "Ī"	U012A # LATIN CAPITAL LETTER I WITH MACRON
<Multi_key> <minus> <I>			: "Ī"	U012A # LATIN CAPITAL LETTER I WITH MACRON
<Multi_key> <I> <minus>			: "Ī"	U012A # LATIN CAPITAL LETTER I WITH MACRON
<dead_macron> <i>			: "ī"	U012B # LATIN SMALL LETTER I WITH MACRON
<Multi_key> <macron> <i>		: "ī"	U012B # LATIN SMALL LETTER I WITH MACRON
<Multi_key> <underscore> <i>		: "ī"	U012B # LATIN SMALL LETTER I WITH MACRON
<Multi_key> <i> <underscore>		: "ī"	U012B # LATIN SMALL LETTER I WITH MACRON
<Multi_key> <minus> <i>			: "ī"	U012B # LATIN SMALL LETTER I WITH MACRON
<Multi_key> <i> <minus>			: "ī"	U012B # LATIN SMALL LETTER I WITH MACRON
<dead_breve> <I>			: "Ĭ"	U012C # LATIN CAPITAL LETTER I WITH BREVE
<Multi_key> <U> <I>			: "Ĭ"	U012C # LATIN CAPITAL LETTER I WITH BREVE
<Multi_key> <u> <I>			: "Ĭ"	U012C # LATIN CAPITAL LETTER I WITH BREVE
<Multi_key> <b> <I>			: "Ĭ"	U012C # LATIN CAPITAL LETTER I WITH BREVE
<dead_breve> <i>			: "ĭ"	U012D # LATIN SMALL LETTER I WITH BREVE
<Multi_key> <U> <i>			: "ĭ"	U012D # LATIN SMALL LETTER I WITH BREVE
<Multi_key> <u> <i>			: "ĭ"	U012D # LATIN SMALL LETTER I WITH BREVE
<Multi_key> <b> <i>			: "ĭ"	U012D # LATIN SMALL LETTER I WITH BREVE
<dead_ogonek> <I>			: "Į"	U012E # LATIN CAPITAL LETTER I WITH OGONEK
<Multi_key> <semicolon> <I>		: "Į"	U012E # LATIN CAPITAL LETTER I WITH OGONEK
<Multi_key> <I> <semicolon>		: "Į"	U012E # LATIN CAPITAL LETTER I WITH OGONEK
<Multi_key> <comma> <I>			: "Į"	U012E # LATIN CAPITAL LETTER I WITH OGONEK
<Multi_key> <I> <comma>			: "Į"	U012E # LATIN CAPITAL LETTER I WITH OGONEK
<dead_ogonek> <i>			: "į"	U012F # LATIN SMALL LETTER I WITH OGONEK
<Multi_key> <semicolon> <i>		: "į"	U012F # LATIN SMALL LETTER I WITH OGONEK
<Multi_key> <i> <semicolon>		: "į"	U012F # LATIN SMALL LETTER I WITH OGONEK
<Multi_key> <comma> <i>			: "į"	U012F # LATIN SMALL LETTER I WITH OGONEK
<Multi_key> <i> <comma>			: "į"	U012F # LATIN SMALL LETTER I WITH OGONEK
<dead_abovedot> <I>			: "İ"	U0130 # LATIN CAPITAL LETTER I WITH DOT ABOVE
<Multi_key> <period> <I>		: "İ"	U0130 # LATIN CAPITAL LETTER I WITH DOT ABOVE
<Multi_key> <I> <period>		: "İ"	U0130 # LATIN CAPITAL LETTER I WITH DOT ABOVE
<dead_abovedot> <i>			: "ı"	U0131 # LATIN SMALL LETTER DOTLESS I
<Multi_key> <i> <period>		: "ı"	U0131 # LATIN SMALL LETTER DOTLESS I
<Multi_key> <period> <i>		: "ı"	U0131 # LATIN SMALL LETTER DOTLESS I
<dead_circumflex> <J>			: "Ĵ"	U0134 # LATIN CAPITAL LETTER J WITH CIRCUMFLEX
<Multi_key> <asciicircum> <J>		: "Ĵ"	U0134 # LATIN CAPITAL LETTER J WITH CIRCUMFLEX
<dead_circumflex> <j>			: "ĵ"	U0135 # LATIN SMALL LETTER J WITH CIRCUMFLEX
<Multi_key> <asciicircum> <j>		: "ĵ"	U0135 # LATIN SMALL LETTER J WITH CIRCUMFLEX
<dead_cedilla> <K>			: "Ķ"	U0136 # LATIN CAPITAL LETTER K WITH CEDILLA
<Multi_key> <comma> <K>			: "Ķ"	U0136 # LATIN CAPITAL LETTER K WITH CEDILLA
<Multi_key> <K> <comma>			: "Ķ"	U0136 # LATIN CAPITAL LETTER K WITH CEDILLA
<Multi_key> <cedilla> <K>		: "Ķ"	U0136 # LATIN CAPITAL LETTER K WITH CEDILLA
<dead_cedilla> <k>			: "ķ"	U0137 # LATIN SMALL LETTER K WITH CEDILLA
<Multi_key> <comma> <k>			: "ķ"	U0137 # LATIN SMALL LETTER K WITH CEDILLA
<Multi_key> <k> <comma>			: "ķ"	U0137 # LATIN SMALL LETTER K WITH CEDILLA
<Multi_key> <cedilla> <k>		: "ķ"	U0137 # LATIN SMALL LETTER K WITH CEDILLA
<Multi_key> <k> <k>			: "ĸ"	U0138 # LATIN SMALL LETTER KRA
<dead_acute> <L>			: "Ĺ"	U0139 # LATIN CAPITAL LETTER L WITH ACUTE
<Multi_key> <acute> <L>			: "Ĺ"	U0139 # LATIN CAPITAL LETTER L WITH ACUTE
<Multi_key> <apostrophe> <L>		: "Ĺ"	U0139 # LATIN CAPITAL LETTER L WITH ACUTE
<Multi_key> <L> <apostrophe>		: "Ĺ"	U0139 # LATIN CAPITAL LETTER L WITH ACUTE
<dead_acute> <l>			: "ĺ"	U013A # LATIN SMALL LETTER L WITH ACUTE
<Multi_key> <acute> <l>			: "ĺ"	U013A # LATIN SMALL LETTER L WITH ACUTE
<Multi_key> <apostrophe> <l>		: "ĺ"	U013A # LATIN SMALL LETTER L WITH ACUTE
<Multi_key> <l> <apostrophe>		: "ĺ"	U013A # LATIN SMALL LETTER L WITH ACUTE
<dead_cedilla> <L>			: "Ļ"	U013B # LATIN CAPITAL LETTER L WITH CEDILLA
<Multi_key> <comma> <L>			: "Ļ"	U013B # LATIN CAPITAL LETTER L WITH CEDILLA
<Multi_key> <L> <comma>			: "Ļ"	U013B # LATIN CAPITAL LETTER L WITH CEDILLA
<Multi_key> <cedilla> <L>		: "Ļ"	U013B # LATIN CAPITAL LETTER L WITH CEDILLA
<dead_cedilla> <l>			: "ļ"	U013C # LATIN SMALL LETTER L WITH CEDILLA
<Multi_key> <comma> <l>			: "ļ"	U013C # LATIN SMALL LETTER L WITH CEDILLA
<Multi_key> <l> <comma>			: "ļ"	U013C # LATIN SMALL LETTER L WITH CEDILLA
<Multi_key> <cedilla> <l>		: "ļ"	U013C # LATIN SMALL LETTER L WITH CEDILLA
<dead_caron> <L>			: "Ľ"	U013D # LATIN CAPITAL LETTER L WITH CARON
<Multi_key> <c> <L>			: "Ľ"	U013D # LATIN CAPITAL LETTER L WITH CARON
<Multi_key> <less> <L>			: "Ľ"	U013D # LATIN CAPITAL LETTER L WITH CARON
<Multi_key> <L> <less>			: "Ľ"	U013D # LATIN CAPITAL LETTER L WITH CARON
<dead_caron> <l>			: "ľ"	U013E # LATIN SMALL LETTER L WITH CARON
<Multi_key> <c> <l>			: "ľ"	U013E # LATIN SMALL LETTER L WITH CARON
<Multi_key> <less> <l>			: "ľ"	U013E # LATIN SMALL LETTER L WITH CARON
<Multi_key> <l> <less>			: "ľ"	U013E # LATIN SMALL LETTER L WITH CARON
<dead_stroke> <L>			: "Ł"	U0141 # LATIN CAPITAL LETTER L WITH STROKE
<Multi_key> <slash> <L>			: "Ł"	U0141 # LATIN CAPITAL LETTER L WITH STROKE
<Multi_key> <L> <slash>			: "Ł"	U0141 # LATIN CAPITAL LETTER L WITH STROKE
<Multi_key> <KP_Divide> <L>		: "Ł"	U0141 # LATIN CAPITAL LETTER L WITH STROKE
<dead_stroke> <l>			: "ł"	U0142 # LATIN SMALL LETTER L WITH STROKE
<Multi_key> <slash> <l>			: "ł"	U0142 # LATIN SMALL LETTER L WITH STROKE
<Multi_key> <l> <slash>			: "ł"	U0142 # LATIN SMALL LETTER L WITH STROKE
<Multi_key> <KP_Divide> <l>		: "ł"	U0142 # LATIN SMALL LETTER L WITH STROKE
<dead_acute> <N>			: "Ń"	U0143 # LATIN CAPITAL LETTER N WITH ACUTE
<Multi_key> <acute> <N>			: "Ń"	U0143 # LATIN CAPITAL LETTER N WITH ACUTE
<Multi_key> <apostrophe> <N>		: "Ń"	U0143 # LATIN CAPITAL LETTER N WITH ACUTE
<Multi_key> <N> <apostrophe>		: "Ń"	U0143 # LATIN CAPITAL LETTER N WITH ACUTE
<dead_acute> <n>			: "ń"	U0144 # LATIN SMALL LETTER N WITH ACUTE
<Multi_key> <acute> <n>			: "ń"	U0144 # LATIN SMALL LETTER N WITH ACUTE
<Multi_key> <apostrophe> <n>		: "ń"	U0144 # LATIN SMALL LETTER N WITH ACUTE
<Multi_key> <n> <apostrophe>		: "ń"	U0144 # LATIN SMALL LETTER N WITH ACUTE
<dead_cedilla> <N>			: "Ņ"	U0145 # LATIN CAPITAL LETTER N WITH CEDILLA
<Multi_key> <comma> <N>			: "Ņ"	U0145 # LATIN CAPITAL LETTER N WITH CEDILLA
<Multi_key> <N> <comma>			: "Ņ"	U0145 # LATIN CAPITAL LETTER N WITH CEDILLA
<Multi_key> <cedilla> <N>		: "Ņ"	U0145 # LATIN CAPITAL LETTER N WITH CEDILLA
<dead_cedilla> <n>			: "ņ"	U0146 # LATIN SMALL LETTER N WITH CEDILLA
<Multi_key> <comma> <n>			: "ņ"	U0146 # LATIN SMALL LETTER N WITH CEDILLA
<Multi_key> <n> <comma>			: "ņ"	U0146 # LATIN SMALL LETTER N WITH CEDILLA
<Multi_key> <cedilla> <n>		: "ņ"	U0146 # LATIN SMALL LETTER N WITH CEDILLA
<dead_caron> <N>			: "Ň"	U0147 # LATIN CAPITAL LETTER N WITH CARON
<Multi_key> <c> <N>			: "Ň"	U0147 # LATIN CAPITAL LETTER N WITH CARON
<Multi_key> <v> <N>			: "Ň"	U0147 # LATIN CAPITAL LETTER N WITH CARON
<Multi_key> <less> <N>			: "Ň"	U0147 # LATIN CAPITAL LETTER N WITH CARON
<Multi_key> <N> <less>			: "Ň"	U0147 # LATIN CAPITAL LETTER N WITH CARON
<dead_caron> <n>			: "ň"	U0148 # LATIN SMALL LETTER N WITH CARON
<Multi_key> <c> <n>			: "ň"	U0148 # LATIN SMALL LETTER N WITH CARON
<Multi_key> <v> <n>			: "ň"	U0148 # LATIN SMALL LETTER N WITH CARON
<Multi_key> <less> <n>			: "ň"	U0148 # LATIN SMALL LETTER N WITH CARON
<Multi_key> <n> <less>			: "ň"	U0148 # LATIN SMALL LETTER N WITH CARON
<Multi_key> <N> <G>			: "Ŋ"	U014A # LATIN CAPITAL LETTER ENG
<Multi_key> <n> <g>			: "ŋ"	U014B # LATIN SMALL LETTER ENG
<dead_macron> <O>			: "Ō"	U014C # LATIN CAPITAL LETTER O WITH MACRON
<Multi_key> <macron> <O>		: "Ō"	U014C # LATIN CAPITAL LETTER O WITH MACRON
<Multi_key> <underscore> <O>		: "Ō"	U014C # LATIN CAPITAL LETTER O WITH MACRON
<Multi_key> <O> <underscore>		: "Ō"	U014C # LATIN CAPITAL LETTER O WITH MACRON
<Multi_key> <minus> <O>			: "Ō"	U014C # LATIN CAPITAL LETTER O WITH MACRON
<Multi_key> <O> <minus>			: "Ō"	U014C # LATIN CAPITAL LETTER O WITH MACRON
<dead_macron> <o>			: "ō"	U014D # LATIN SMALL LETTER O WITH MACRON
<Multi_key> <macron> <o>		: "ō"	U014D # LATIN SMALL LETTER O WITH MACRON
<Multi_key> <underscore> <o>		: "ō"	U014D # LATIN SMALL LETTER O WITH MACRON
<Multi_key> <o> <underscore>		: "ō"	U014D # LATIN SMALL LETTER O WITH MACRON
<Multi_key> <minus> <o>			: "ō"	U014D # LATIN SMALL LETTER O WITH MACRON
<Multi_key> <o> <minus>			: "ō"	U014D # LATIN SMALL LETTER O WITH MACRON
<dead_breve> <O>			: "Ŏ"	U014E # LATIN CAPITAL LETTER O WITH BREVE
<Multi_key> <U> <O>			: "Ŏ"	U014E # LATIN CAPITAL LETTER O WITH BREVE
<Multi_key> <u> <O>			: "Ŏ"	U014E # LATIN CAPITAL LETTER O WITH BREVE
<Multi_key> <b> <O>			: "Ŏ"	U014E # LATIN CAPITAL LETTER O WITH BREVE
<dead_breve> <o>			: "ŏ"	U014F # LATIN SMALL LETTER O WITH BREVE
<Multi_key> <U> <o>			: "ŏ"	U014F # LATIN SMALL LETTER O WITH BREVE
<Multi_key> <u> <o>			: "ŏ"	U014F # LATIN SMALL LETTER O WITH BREVE
<Multi_key> <b> <o>			: "ŏ"	U014F # LATIN SMALL LETTER O WITH BREVE
<dead_doubleacute> <O>			: "Ő"	U0150 # LATIN CAPITAL LETTER O WITH DOUBLE ACUTE
<Multi_key> <equal> <O>			: "Ő"	U0150 # LATIN CAPITAL LETTER O WITH DOUBLE ACUTE
<dead_doubleacute> <o>			: "ő"	U0151 # LATIN SMALL LETTER O WITH DOUBLE ACUTE
<Multi_key> <equal> <o>			: "ő"	U0151 # LATIN SMALL LETTER O WITH DOUBLE ACUTE
<dead_acute> <R>			: "Ŕ"	U0154 # LATIN CAPITAL LETTER R WITH ACUTE
<Multi_key> <acute> <R>			: "Ŕ"	U0154 # LATIN CAPITAL LETTER R WITH ACUTE
<Multi_key> <apostrophe> <R>		: "Ŕ"	U0154 # LATIN CAPITAL LETTER R WITH ACUTE
<Multi_key> <R> <apostrophe>		: "Ŕ"	U0154 # LATIN CAPITAL LETTER R WITH ACUTE
<dead_acute> <r>			: "ŕ"	U0155 # LATIN SMALL LETTER R WITH ACUTE
<Multi_key> <acute> <r>			: "ŕ"	U0155 # LATIN SMALL LETTER R WITH ACUTE
<Multi_key> <apostrophe> <r>		: "ŕ"	U0155 # LATIN SMALL LETTER R WITH ACUTE
<Multi_key> <r> <apostrophe>		: "ŕ"	U0155 # LATIN SMALL LETTER R WITH ACUTE
<dead_cedilla> <R>			: "Ŗ"	U0156 # LATIN CAPITAL LETTER R WITH CEDILLA
<Multi_key> <comma> <R>			: "Ŗ"	U0156 # LATIN CAPITAL LETTER R WITH CEDILLA
<Multi_key> <R> <comma>			: "Ŗ"	U0156 # LATIN CAPITAL LETTER R WITH CEDILLA
<Multi_key> <cedilla> <R>		: "Ŗ"	U0156 # LATIN CAPITAL LETTER R WITH CEDILLA
<dead_cedilla> <r>			: "ŗ"	U0157 # LATIN SMALL LETTER R WITH CEDILLA
<Multi_key> <comma> <r>			: "ŗ"	U0157 # LATIN SMALL LETTER R WITH CEDILLA
<Multi_key> <r> <comma>			: "ŗ"	U0157 # LATIN SMALL LETTER R WITH CEDILLA
<Multi_key> <cedilla> <r>		: "ŗ"	U0157 # LATIN SMALL LETTER R WITH CEDILLA
<dead_caron> <R>			: "Ř"	U0158 # LATIN CAPITAL LETTER R WITH CARON
<Multi_key> <c> <R>			: "Ř"	U0158 # LATIN CAPITAL LETTER R WITH CARON
<Multi_key> <v> <R>			: "Ř"	U0158 # LATIN CAPITAL LETTER R WITH CARON
<Multi_key> <less> <R>			: "Ř"	U0158 # LATIN CAPITAL LETTER R WITH CARON
<Multi_key> <R> <less>			: "Ř"	U0158 # LATIN CAPITAL LETTER R WITH CARON
<dead_caron> <r>			: "ř"	U0159 # LATIN SMALL LETTER R WITH CARON
<Multi_key> <c> <r>			: "ř"	U0159 # LATIN SMALL LETTER R WITH CARON
<Multi_key> <v> <r>			: "ř"	U0159 # LATIN SMALL LETTER R WITH CARON
<Multi_key> <less> <r>			: "ř"	U0159 # LATIN SMALL LETTER R WITH CARON
<Multi_key> <r> <less>			: "ř"	U0159 # LATIN SMALL LETTER R WITH CARON
<dead_acute> <S>			: "Ś"	U015A # LATIN CAPITAL LETTER S WITH ACUTE
<Multi_key> <acute> <S>			: "Ś"	U015A # LATIN CAPITAL LETTER S WITH ACUTE
<Multi_key> <apostrophe> <S>		: "Ś"	U015A # LATIN CAPITAL LETTER S WITH ACUTE
<Multi_key> <S> <apostrophe>		: "Ś"	U015A # LATIN CAPITAL LETTER S WITH ACUTE
<dead_acute> <s>			: "ś"	U015B # LATIN SMALL LETTER S WITH ACUTE
<Multi_key> <acute> <s>			: "ś"	U015B # LATIN SMALL LETTER S WITH ACUTE
<Multi_key> <apostrophe> <s>		: "ś"	U015B # LATIN SMALL LETTER S WITH ACUTE
<Multi_key> <s> <apostrophe>		: "ś"	U015B # LATIN SMALL LETTER S WITH ACUTE
<dead_circumflex> <S>			: "Ŝ"	U015C # LATIN CAPITAL LETTER S WITH CIRCUMFLEX
<Multi_key> <asciicircum> <S>		: "Ŝ"	U015C # LATIN CAPITAL LETTER S WITH CIRCUMFLEX
<dead_circumflex> <s>			: "ŝ"	U015D # LATIN SMALL LETTER S WITH CIRCUMFLEX
<Multi_key> <asciicircum> <s>		: "ŝ"	U015D # LATIN SMALL LETTER S WITH CIRCUMFLEX
<dead_cedilla> <S>			: "Ş"	U015E # LATIN CAPITAL LETTER S WITH CEDILLA
<Multi_key> <comma> <S>			: "Ş"	U015E # LATIN CAPITAL LETTER S WITH CEDILLA
<Multi_key> <S> <comma>			: "Ş"	U015E # LATIN CAPITAL LETTER S WITH CEDILLA
<Multi_key> <cedilla> <S>		: "Ş"	U015E # LATIN CAPITAL LETTER S WITH CEDILLA
<dead_cedilla> <s>			: "ş"	U015F # LATIN SMALL LETTER S WITH CEDILLA
<Multi_key> <comma> <s>			: "ş"	U015F # LATIN SMALL LETTER S WITH CEDILLA
<Multi_key> <s> <comma>			: "ş"	U015F # LATIN SMALL LETTER S WITH CEDILLA
<Multi_key> <cedilla> <s>		: "ş"	U015F # LATIN SMALL LETTER S WITH CEDILLA
<Multi_key> <s> <cedilla>		: "ş"	U015F # LATIN SMALL LETTER S WITH CEDILLA
<dead_caron> <S>			: "Š"	U0160 # LATIN CAPITAL LETTER S WITH CARON
<Multi_key> <c> <S>			: "Š"	U0160 # LATIN CAPITAL LETTER S WITH CARON
<Multi_key> <v> <S>			: "Š"	U0160 # LATIN CAPITAL LETTER S WITH CARON
<Multi_key> <less> <S>			: "Š"	U0160 # LATIN CAPITAL LETTER S WITH CARON
<Multi_key> <S> <less>			: "Š"	U0160 # LATIN CAPITAL LETTER S WITH CARON
<dead_caron> <s>			: "š"	U0161 # LATIN SMALL LETTER S WITH CARON
<Multi_key> <c> <s>			: "š"	U0161 # LATIN SMALL LETTER S WITH CARON
<Multi_key> <v> <s>			: "š"	U0161 # LATIN SMALL LETTER S WITH CARON
<Multi_key> <less> <s>			: "š"	U0161 # LATIN SMALL LETTER S WITH CARON
<Multi_key> <s> <less>			: "š"	U0161 # LATIN SMALL LETTER S WITH CARON
<dead_cedilla> <T>			: "Ţ"	U0162 # LATIN CAPITAL LETTER T WITH CEDILLA
<Multi_key> <comma> <T>			: "Ţ"	U0162 # LATIN CAPITAL LETTER T WITH CEDILLA
<Multi_key> <T> <comma>			: "Ţ"	U0162 # LATIN CAPITAL LETTER T WITH CEDILLA
<Multi_key> <cedilla> <T>		: "Ţ"	U0162 # LATIN CAPITAL LETTER T WITH CEDILLA
<dead_cedilla> <t>			: "ţ"	U0163 # LATIN SMALL LETTER T WITH CEDILLA
<Multi_key> <comma> <t>			: "ţ"	U0163 # LATIN SMALL LETTER T WITH CEDILLA
<Multi_key> <t> <comma>			: "ţ"	U0163 # LATIN SMALL LETTER T WITH CEDILLA
<Multi_key> <cedilla> <t>		: "ţ"	U0163 # LATIN SMALL LETTER T WITH CEDILLA
<dead_caron> <T>			: "Ť"	U0164 # LATIN CAPITAL LETTER T WITH CARON
<Multi_key> <c> <T>			: "Ť"	U0164 # LATIN CAPITAL LETTER T WITH CARON
<Multi_key> <v> <T>			: "Ť"	U0164 # LATIN CAPITAL LETTER T WITH CARON
<Multi_key> <less> <T>			: "Ť"	U0164 # LATIN CAPITAL LETTER T WITH CARON
<Multi_key> <T> <less>			: "Ť"	U0164 # LATIN CAPITAL LETTER T WITH CARON
<dead_caron> <t>			: "ť"	U0165 # LATIN SMALL LETTER T WITH CARON
<Multi_key> <c> <t>			: "ť"	U0165 # LATIN SMALL LETTER T WITH CARON
<Multi_key> <v> <t>			: "ť"	U0165 # LATIN SMALL LETTER T WITH CARON
<Multi_key> <less> <t>			: "ť"	U0165 # LATIN SMALL LETTER T WITH CARON
<Multi_key> <t> <less>			: "ť"	U0165 # LATIN SMALL LETTER T WITH CARON
<dead_stroke> <T>			: "Ŧ"	U0166 # LATIN CAPITAL LETTER T WITH STROKE
<Multi_key> <slash> <T>			: "Ŧ"	U0166 # LATIN CAPITAL LETTER T WITH STROKE
<Multi_key> <KP_Divide> <T>		: "Ŧ"	U0166 # LATIN CAPITAL LETTER T WITH STROKE
<Multi_key> <T> <slash>			: "Ŧ"	U0166 # LATIN CAPITAL LETTER T WITH STROKE
<Multi_key> <T> <minus>			: "Ŧ"	U0166 # LATIN CAPITAL LETTER T WITH STROKE
<dead_stroke> <t>			: "ŧ"	U0167 # LATIN SMALL LETTER T WITH STROKE
<Multi_key> <slash> <t>			: "ŧ"	U0167 # LATIN SMALL LETTER T WITH STROKE
<Multi_key> <KP_Divide> <t>		: "ŧ"	U0167 # LATIN SMALL LETTER T WITH STROKE
<Multi_key> <t> <slash>			: "ŧ"	U0167 # LATIN SMALL LETTER T WITH STROKE
<Multi_key> <t> <minus>			: "ŧ"	U0167 # LATIN SMALL LETTER T WITH STROKE
<dead_tilde> <U>			: "Ũ"	U0168 # LATIN CAPITAL LETTER U WITH TILDE
<Multi_key> <asciitilde> <U>		: "Ũ"	U0168 # LATIN CAPITAL LETTER U WITH TILDE
<Multi_key> <U> <asciitilde>		: "Ũ"	U0168 # LATIN CAPITAL LETTER U WITH TILDE
<dead_tilde> <u>			: "ũ"	U0169 # LATIN SMALL LETTER U WITH TILDE
<Multi_key> <asciitilde> <u>		: "ũ"	U0169 # LATIN SMALL LETTER U WITH TILDE
<Multi_key> <u> <asciitilde>		: "ũ"	U0169 # LATIN SMALL LETTER U WITH TILDE
<dead_macron> <U>			: "Ū"	U016A # LATIN CAPITAL LETTER U WITH MACRON
<Multi_key> <macron> <U>		: "Ū"	U016A # LATIN CAPITAL LETTER U WITH MACRON
<Multi_key> <underscore> <U>		: "Ū"	U016A # LATIN CAPITAL LETTER U WITH MACRON
<Multi_key> <U> <underscore>		: "Ū"	U016A # LATIN CAPITAL LETTER U WITH MACRON
<Multi_key> <minus> <U>			: "Ū"	U016A # LATIN CAPITAL LETTER U WITH MACRON
<Multi_key> <U> <minus>			: "Ū"	U016A # LATIN CAPITAL LETTER U WITH MACRON
<dead_macron> <u>			: "ū"	U016B # LATIN SMALL LETTER U WITH MACRON
<Multi_key> <macron> <u>		: "ū"	U016B # LATIN SMALL LETTER U WITH MACRON
<Multi_key> <underscore> <u>		: "ū"	U016B # LATIN SMALL LETTER U WITH MACRON
<Multi_key> <u> <underscore>		: "ū"	U016B # LATIN SMALL LETTER U WITH MACRON
<Multi_key> <minus> <u>			: "ū"	U016B # LATIN SMALL LETTER U WITH MACRON
<Multi_key> <u> <minus>			: "ū"	U016B # LATIN SMALL LETTER U WITH MACRON
<dead_breve> <U>			: "Ŭ"	U016C # LATIN CAPITAL LETTER U WITH BREVE
<Multi_key> <U> <U>			: "Ŭ"	U016C # LATIN CAPITAL LETTER U WITH BREVE
<Multi_key> <u> <U>			: "Ŭ"	U016C # LATIN CAPITAL LETTER U WITH BREVE
<Multi_key> <b> <U>			: "Ŭ"	U016C # LATIN CAPITAL LETTER U WITH BREVE
<dead_breve> <u>			: "ŭ"	U016D # LATIN SMALL LETTER U WITH BREVE
<Multi_key> <U> <u>			: "ŭ"	U016D # LATIN SMALL LETTER U WITH BREVE
<Multi_key> <u> <u>			: "ŭ"	U016D # LATIN SMALL LETTER U WITH BREVE
<Multi_key> <b> <u>			: "ŭ"	U016D # LATIN SMALL LETTER U WITH BREVE
<dead_abovering> <U>			: "Ů"	U016E # LATIN CAPITAL LETTER U WITH RING ABOVE
<Multi_key> <o> <U>			: "Ů"	U016E # LATIN CAPITAL LETTER U WITH RING ABOVE
<Multi_key> <asterisk> <U>		: "Ů"	U016E # LATIN CAPITAL LETTER U WITH RING ABOVE
<Multi_key> <U> <asterisk>		: "Ů"	U016E # LATIN CAPITAL LETTER U WITH RING ABOVE
<dead_abovering> <u>			: "ů"	U016F # LATIN SMALL LETTER U WITH RING ABOVE
<Multi_key> <o> <u>			: "ů"	U016F # LATIN SMALL LETTER U WITH RING ABOVE
<Multi_key> <asterisk> <u>		: "ů"	U016F # LATIN SMALL LETTER U WITH RING ABOVE
<Multi_key> <u> <asterisk>		: "ů"	U016F # LATIN SMALL LETTER U WITH RING ABOVE
<dead_doubleacute> <U>			: "Ű"	U0170 # LATIN CAPITAL LETTER U WITH DOUBLE ACUTE
<Multi_key> <equal> <U>			: "Ű"	U0170 # LATIN CAPITAL LETTER U WITH DOUBLE ACUTE
<dead_doubleacute> <u>			: "ű"	U0171 # LATIN SMALL LETTER U WITH DOUBLE ACUTE
<Multi_key> <equal> <u>			: "ű"	U0171 # LATIN SMALL LETTER U WITH DOUBLE ACUTE
<dead_ogonek> <U>			: "Ų"	U0172 # LATIN CAPITAL LETTER U WITH OGONEK
<Multi_key> <semicolon> <U>		: "Ų"	U0172 # LATIN CAPITAL LETTER U WITH OGONEK
<Multi_key> <U> <semicolon>		: "Ų"	U0172 # LATIN CAPITAL LETTER U WITH OGONEK
<Multi_key> <comma> <U>			: "Ų"	U0172 # LATIN CAPITAL LETTER U WITH OGONEK
<Multi_key> <U> <comma>			: "Ų"	U0172 # LATIN CAPITAL LETTER U WITH OGONEK
<dead_ogonek> <u>			: "ų"	U0173 # LATIN SMALL LETTER U WITH OGONEK
<Multi_key> <semicolon> <u>		: "ų"	U0173 # LATIN SMALL LETTER U WITH OGONEK
<Multi_key> <u> <semicolon>		: "ų"	U0173 # LATIN SMALL LETTER U WITH OGONEK
<Multi_key> <comma> <u>			: "ų"	U0173 # LATIN SMALL LETTER U WITH OGONEK
<Multi_key> <u> <comma>			: "ų"	U0173 # LATIN SMALL LETTER U WITH OGONEK
<dead_circumflex> <W>			: "Ŵ"	U0174 # LATIN CAPITAL LETTER W WITH CIRCUMFLEX
<Multi_key> <asciicircum> <W>		: "Ŵ"	U0174 # LATIN CAPITAL LETTER W WITH CIRCUMFLEX
<Multi_key> <W> <asciicircum>		: "Ŵ"	U0174 # LATIN CAPITAL LETTER W WITH CIRCUMFLEX
<dead_circumflex> <w>			: "ŵ"	U0175 # LATIN SMALL LETTER W WITH CIRCUMFLEX
<Multi_key> <asciicircum> <w>		: "ŵ"	U0175 # LATIN SMALL LETTER W WITH CIRCUMFLEX
<Multi_key> <w> <asciicircum>		: "ŵ"	U0175 # LATIN SMALL LETTER W WITH CIRCUMFLEX
<dead_circumflex> <Y>			: "Ŷ"	U0176 # LATIN CAPITAL LETTER Y WITH CIRCUMFLEX
<Multi_key> <asciicircum> <Y>		: "Ŷ"	U0176 # LATIN CAPITAL LETTER Y WITH CIRCUMFLEX
<Multi_key> <Y> <asciicircum>		: "Ŷ"	U0176 # LATIN CAPITAL LETTER Y WITH CIRCUMFLEX
<dead_circumflex> <y>			: "ŷ"	U0177 # LATIN SMALL LETTER Y WITH CIRCUMFLEX
<Multi_key> <asciicircum> <y>		: "ŷ"	U0177 # LATIN SMALL LETTER Y WITH CIRCUMFLEX
<Multi_key> <y> <asciicircum>		: "ŷ"	U0177 # LATIN SMALL LETTER Y WITH CIRCUMFLEX
<dead_diaeresis> <Y>			: "Ÿ"	U0178 # LATIN CAPITAL LETTER Y WITH DIAERESIS
<Multi_key> <quotedbl> <Y>		: "Ÿ"	U0178 # LATIN CAPITAL LETTER Y WITH DIAERESIS
<Multi_key> <Y> <quotedbl>		: "Ÿ"	U0178 # LATIN CAPITAL LETTER Y WITH DIAERESIS
<Multi_key> <diaeresis> <Y>		: "Ÿ"	U0178 # LATIN CAPITAL LETTER Y WITH DIAERESIS
<Multi_key> <Y> <diaeresis>		: "Ÿ"	U0178 # LATIN CAPITAL LETTER Y WITH DIAERESIS
<dead_acute> <Z>			: "Ź"	U0179 # LATIN CAPITAL LETTER Z WITH ACUTE
<Multi_key> <acute> <Z>			: "Ź"	U0179 # LATIN CAPITAL LETTER Z WITH ACUTE
<Multi_key> <apostrophe> <Z>		: "Ź"	U0179 # LATIN CAPITAL LETTER Z WITH ACUTE
<Multi_key> <Z> <apostrophe>		: "Ź"	U0179 # LATIN CAPITAL LETTER Z WITH ACUTE
<dead_acute> <z>			: "ź"	U017A # LATIN SMALL LETTER Z WITH ACUTE
<Multi_key> <acute> <z>			: "ź"	U017A # LATIN SMALL LETTER Z WITH ACUTE
<Multi_key> <apostrophe> <z>		: "ź"	U017A # LATIN SMALL LETTER Z WITH ACUTE
<Multi_key> <z> <apostrophe>		: "ź"	U017A # LATIN SMALL LETTER Z WITH ACUTE
<dead_abovedot> <Z>			: "Ż"	U017B # LATIN CAPITAL LETTER Z WITH DOT ABOVE
<Multi_key> <period> <Z>		: "Ż"	U017B # LATIN CAPITAL LETTER Z WITH DOT ABOVE
<Multi_key> <Z> <period>		: "Ż"	U017B # LATIN CAPITAL LETTER Z WITH DOT ABOVE
<dead_abovedot> <z>			: "ż"	U017C # LATIN SMALL LETTER Z WITH DOT ABOVE
<Multi_key> <period> <z>		: "ż"	U017C # LATIN SMALL LETTER Z WITH DOT ABOVE
<Multi_key> <z> <period>		: "ż"	U017C # LATIN SMALL LETTER Z WITH DOT ABOVE
<dead_caron> <Z>			: "Ž"	U017D # LATIN CAPITAL LETTER Z WITH CARON
<Multi_key> <c> <Z>			: "Ž"	U017D # LATIN CAPITAL LETTER Z WITH CARON
<Multi_key> <v> <Z>			: "Ž"	U017D # LATIN CAPITAL LETTER Z WITH CARON
<Multi_key> <less> <Z>			: "Ž"	U017D # LATIN CAPITAL LETTER Z WITH CARON
<Multi_key> <Z> <less>			: "Ž"	U017D # LATIN CAPITAL LETTER Z WITH CARON
<dead_caron> <z>			: "ž"	U017E # LATIN SMALL LETTER Z WITH CARON
<Multi_key> <c> <z>			: "ž"	U017E # LATIN SMALL LETTER Z WITH CARON
<Multi_key> <v> <z>			: "ž"	U017E # LATIN SMALL LETTER Z WITH CARON
<Multi_key> <less> <z>			: "ž"	U017E # LATIN SMALL LETTER Z WITH CARON
<Multi_key> <z> <less>			: "ž"	U017E # LATIN SMALL LETTER Z WITH CARON
<Multi_key> <f> <s>			: "ſ"	U017F # LATIN SMALL LETTER LONG S
<Multi_key> <f> <S>			: "ſ"	U017F # LATIN SMALL LETTER LONG S
# Latin Extended-B
<dead_stroke> <b>				: "ƀ"	U0180 # LATIN SMALL LETTER B WITH STROKE
<Multi_key> <slash> <b>				: "ƀ"	U0180 # LATIN SMALL LETTER B WITH STROKE
<Multi_key> <KP_Divide> <b>			: "ƀ"	U0180 # LATIN SMALL LETTER B WITH STROKE
<Multi_key> <E> <E>				: "Ə"	U018F # LATIN CAPITAL LETTER SCHWA
<dead_stroke> <I>				: "Ɨ"	U0197 # LATIN CAPITAL LETTER I WITH STROKE
<Multi_key> <slash> <I>				: "Ɨ"	U0197 # LATIN CAPITAL LETTER I WITH STROKE
<Multi_key> <KP_Divide> <I>			: "Ɨ"	U0197 # LATIN CAPITAL LETTER I WITH STROKE
<dead_horn> <O>					: "Ơ"	U01A0 # LATIN CAPITAL LETTER O WITH HORN
<Multi_key> <plus> <O>				: "Ơ"	U01A0 # LATIN CAPITAL LETTER O WITH HORN
<dead_horn> <o>					: "ơ"	U01A1 # LATIN SMALL LETTER O WITH HORN
<Multi_key> <plus> <o>				: "ơ"	U01A1 # LATIN SMALL LETTER O WITH HORN
<dead_horn> <U>					: "Ư"	U01AF # LATIN CAPITAL LETTER U WITH HORN
<Multi_key> <plus> <U>				: "Ư"	U01AF # LATIN CAPITAL LETTER U WITH HORN
<dead_horn> <u>					: "ư"	U01B0 # LATIN SMALL LETTER U WITH HORN
<Multi_key> <plus> <u>				: "ư"	U01B0 # LATIN SMALL LETTER U WITH HORN
<dead_stroke> <Z>				: "Ƶ"	U01B5 # LATIN CAPITAL LETTER Z WITH STROKE
<Multi_key> <slash> <Z>				: "Ƶ"	U01B5 # LATIN CAPITAL LETTER Z WITH STROKE
<Multi_key> <KP_Divide> <Z>			: "Ƶ"	U01B5 # LATIN CAPITAL LETTER Z WITH STROKE
<dead_stroke> <z>				: "ƶ"	U01B6 # LATIN SMALL LETTER Z WITH STROKE
<Multi_key> <slash> <z>				: "ƶ"	U01B6 # LATIN SMALL LETTER Z WITH STROKE
<Multi_key> <KP_Divide> <z>			: "ƶ"	U01B6 # LATIN SMALL LETTER Z WITH STROKE
<dead_caron> <A>				: "Ǎ"	U01CD # LATIN CAPITAL LETTER A WITH CARON
<Multi_key> <c> <A>				: "Ǎ"	U01CD # LATIN CAPITAL LETTER A WITH CARON
<Multi_key> <v> <A>				: "Ǎ"	U01CD # LATIN CAPITAL LETTER A WITH CARON
<dead_caron> <a>				: "ǎ"	U01CE # LATIN SMALL LETTER A WITH CARON
<Multi_key> <c> <a>				: "ǎ"	U01CE # LATIN SMALL LETTER A WITH CARON
<Multi_key> <v> <a>				: "ǎ"	U01CE # LATIN SMALL LETTER A WITH CARON
<dead_caron> <I>				: "Ǐ"	U01CF # LATIN CAPITAL LETTER I WITH CARON
<Multi_key> <c> <I>				: "Ǐ"	U01CF # LATIN CAPITAL LETTER I WITH CARON
<Multi_key> <v> <I>				: "Ǐ"	U01CF # LATIN CAPITAL LETTER I WITH CARON
<dead_caron> <i>				: "ǐ"	U01D0 # LATIN SMALL LETTER I WITH CARON
<Multi_key> <c> <i>				: "ǐ"	U01D0 # LATIN SMALL LETTER I WITH CARON
<Multi_key> <v> <i>				: "ǐ"	U01D0 # LATIN SMALL LETTER I WITH CARON
<dead_caron> <O>				: "Ǒ"	U01D1 # LATIN CAPITAL LETTER O WITH CARON
<Multi_key> <c> <O>				: "Ǒ"	U01D1 # LATIN CAPITAL LETTER O WITH CARON
<Multi_key> <v> <O>				: "Ǒ"	U01D1 # LATIN CAPITAL LETTER O WITH CARON
<dead_caron> <o>				: "ǒ"	U01D2 # LATIN SMALL LETTER O WITH CARON
<Multi_key> <c> <o>				: "ǒ"	U01D2 # LATIN SMALL LETTER O WITH CARON
<Multi_key> <v> <o>				: "ǒ"	U01D2 # LATIN SMALL LETTER O WITH CARON
<dead_caron> <U>				: "Ǔ"	U01D3 # LATIN CAPITAL LETTER U WITH CARON
<Multi_key> <c> <U>				: "Ǔ"	U01D3 # LATIN CAPITAL LETTER U WITH CARON
<Multi_key> <v> <U>				: "Ǔ"	U01D3 # LATIN CAPITAL LETTER U WITH CARON
<dead_caron> <u>				: "ǔ"	U01D4 # LATIN SMALL LETTER U WITH CARON
<Multi_key> <c> <u>				: "ǔ"	U01D4 # LATIN SMALL LETTER U WITH CARON
<Multi_key> <v> <u>				: "ǔ"	U01D4 # LATIN SMALL LETTER U WITH CARON
<dead_macron> <Udiaeresis>			: "Ǖ"	U01D5 # LATIN CAPITAL LETTER U WITH DIAERESIS AND MACRON
<Multi_key> <macron> <Udiaeresis>		: "Ǖ"	U01D5 # LATIN CAPITAL LETTER U WITH DIAERESIS AND MACRON
<Multi_key> <underscore> <Udiaeresis>		: "Ǖ"	U01D5 # LATIN CAPITAL LETTER U WITH DIAERESIS AND MACRON
<dead_macron> <dead_diaeresis> <U>		: "Ǖ"	U01D5 # LATIN CAPITAL LETTER U WITH DIAERESIS AND MACRON
<dead_macron> <Multi_key> <quotedbl> <U>	: "Ǖ"	U01D5 # LATIN CAPITAL LETTER U WITH DIAERESIS AND MACRON
<Multi_key> <macron> <dead_diaeresis> <U>	: "Ǖ"	U01D5 # LATIN CAPITAL LETTER U WITH DIAERESIS AND MACRON
<Multi_key> <macron> <quotedbl> <U>		: "Ǖ"	U01D5 # LATIN CAPITAL LETTER U WITH DIAERESIS AND MACRON
<Multi_key> <underscore> <dead_diaeresis> <U>	: "Ǖ"	U01D5 # LATIN CAPITAL LETTER U WITH DIAERESIS AND MACRON
<Multi_key> <underscore> <quotedbl> <U>		: "Ǖ"	U01D5 # LATIN CAPITAL LETTER U WITH DIAERESIS AND MACRON
<dead_macron> <udiaeresis>			: "ǖ"	U01D6 # LATIN SMALL LETTER U WITH DIAERESIS AND MACRON
<Multi_key> <macron> <udiaeresis>		: "ǖ"	U01D6 # LATIN SMALL LETTER U WITH DIAERESIS AND MACRON
<Multi_key> <underscore> <udiaeresis>		: "ǖ"	U01D6 # LATIN SMALL LETTER U WITH DIAERESIS AND MACRON
<dead_macron> <dead_diaeresis> <u>		: "ǖ"	U01D6 # LATIN SMALL LETTER U WITH DIAERESIS AND MACRON
<dead_macron> <Multi_key> <quotedbl> <u>	: "ǖ"	U01D6 # LATIN SMALL LETTER U WITH DIAERESIS AND MACRON
<Multi_key> <macron> <dead_diaeresis> <u>	: "ǖ"	U01D6 # LATIN SMALL LETTER U WITH DIAERESIS AND MACRON
<Multi_key> <macron> <quotedbl> <u>		: "ǖ"	U01D6 # LATIN SMALL LETTER U WITH DIAERESIS AND MACRON
<Multi_key> <underscore> <dead_diaeresis> <u>	: "ǖ"	U01D6 # LATIN SMALL LETTER U WITH DIAERESIS AND MACRON
<Multi_key> <underscore> <quotedbl> <u>		: "ǖ"	U01D6 # LATIN SMALL LETTER U WITH DIAERESIS AND MACRON
<dead_acute> <Udiaeresis>			: "Ǘ"	U01D7 # LATIN CAPITAL LETTER U WITH DIAERESIS AND ACUTE
<Multi_key> <acute> <Udiaeresis>		: "Ǘ"	U01D7 # LATIN CAPITAL LETTER U WITH DIAERESIS AND ACUTE
<Multi_key> <apostrophe> <Udiaeresis>		: "Ǘ"	U01D7 # LATIN CAPITAL LETTER U WITH DIAERESIS AND ACUTE
<dead_acute> <dead_diaeresis> <U>		: "Ǘ"	U01D7 # LATIN CAPITAL LETTER U WITH DIAERESIS AND ACUTE
<dead_acute> <Multi_key> <quotedbl> <U>		: "Ǘ"	U01D7 # LATIN CAPITAL LETTER U WITH DIAERESIS AND ACUTE
<Multi_key> <acute> <dead_diaeresis> <U>	: "Ǘ"	U01D7 # LATIN CAPITAL LETTER U WITH DIAERESIS AND ACUTE
<Multi_key> <acute> <quotedbl> <U>		: "Ǘ"	U01D7 # LATIN CAPITAL LETTER U WITH DIAERESIS AND ACUTE
<Multi_key> <apostrophe> <dead_diaeresis> <U>	: "Ǘ"	U01D7 # LATIN CAPITAL LETTER U WITH DIAERESIS AND ACUTE
<Multi_key> <apostrophe> <quotedbl> <U>		: "Ǘ"	U01D7 # LATIN CAPITAL LETTER U WITH DIAERESIS AND ACUTE
<dead_acute> <udiaeresis>			: "ǘ"	U01D8 # LATIN SMALL LETTER U WITH DIAERESIS AND ACUTE
<Multi_key> <acute> <udiaeresis>		: "ǘ"	U01D8 # LATIN SMALL LETTER U WITH DIAERESIS AND ACUTE
<Multi_key> <apostrophe> <udiaeresis>		: "ǘ"	U01D8 # LATIN SMALL LETTER U WITH DIAERESIS AND ACUTE
<dead_acute> <dead_diaeresis> <u>		: "ǘ"	U01D8 # LATIN SMALL LETTER U WITH DIAERESIS AND ACUTE
<dead_acute> <Multi_key> <quotedbl> <u>		: "ǘ"	U01D8 # LATIN SMALL LETTER U WITH DIAERESIS AND ACUTE
<Multi_key> <acute> <dead_diaeresis> <u>	: "ǘ"	U01D8 # LATIN SMALL LETTER U WITH DIAERESIS AND ACUTE
<Multi_key> <acute> <quotedbl> <u>		: "ǘ"	U01D8 # LATIN SMALL LETTER U WITH DIAERESIS AND ACUTE
<Multi_key> <apostrophe> <dead_diaeresis> <u>	: "ǘ"	U01D8 # LATIN SMALL LETTER U WITH DIAERESIS AND ACUTE
<Multi_key> <apostrophe> <quotedbl> <u>		: "ǘ"	U01D8 # LATIN SMALL LETTER U WITH DIAERESIS AND ACUTE
<dead_caron> <Udiaeresis>			: "Ǚ"	U01D9 # LATIN CAPITAL LETTER U WITH DIAERESIS AND CARON
<Multi_key> <c> <Udiaeresis>			: "Ǚ"	U01D9 # LATIN CAPITAL LETTER U WITH DIAERESIS AND CARON
<dead_caron> <dead_diaeresis> <U>		: "Ǚ"	U01D9 # LATIN CAPITAL LETTER U WITH DIAERESIS AND CARON
<dead_caron> <Multi_key> <quotedbl> <U>		: "Ǚ"	U01D9 # LATIN CAPITAL LETTER U WITH DIAERESIS AND CARON
<Multi_key> <c> <dead_diaeresis> <U>		: "Ǚ"	U01D9 # LATIN CAPITAL LETTER U WITH DIAERESIS AND CARON
<Multi_key> <c> <quotedbl> <U>			: "Ǚ"	U01D9 # LATIN CAPITAL LETTER U WITH DIAERESIS AND CARON
<dead_caron> <udiaeresis>			: "ǚ"	U01DA # LATIN SMALL LETTER U WITH DIAERESIS AND CARON
<Multi_key> <c> <udiaeresis>			: "ǚ"	U01DA # LATIN SMALL LETTER U WITH DIAERESIS AND CARON
<dead_caron> <dead_diaeresis> <u>		: "ǚ"	U01DA # LATIN SMALL LETTER U WITH DIAERESIS AND CARON
<dead_caron> <Multi_key> <quotedbl> <u>		: "ǚ"	U01DA # LATIN SMALL LETTER U WITH DIAERESIS AND CARON
<Multi_key> <c> <dead_diaeresis> <u>		: "ǚ"	U01DA # LATIN SMALL LETTER U WITH DIAERESIS AND CARON
<Multi_key> <c> <quotedbl> <u>			: "ǚ"	U01DA # LATIN SMALL LETTER U WITH DIAERESIS AND CARON
<dead_grave> <Udiaeresis>			: "Ǜ"	U01DB # LATIN CAPITAL LETTER U WITH DIAERESIS AND GRAVE
<Multi_key> <grave> <Udiaeresis>		: "Ǜ"	U01DB # LATIN CAPITAL LETTER U WITH DIAERESIS AND GRAVE
<dead_grave> <dead_diaeresis> <U>		: "Ǜ"	U01DB # LATIN CAPITAL LETTER U WITH DIAERESIS AND GRAVE
<dead_grave> <Multi_key> <quotedbl> <U>		: "Ǜ"	U01DB # LATIN CAPITAL LETTER U WITH DIAERESIS AND GRAVE
<Multi_key> <grave> <dead_diaeresis> <U>	: "Ǜ"	U01DB # LATIN CAPITAL LETTER U WITH DIAERESIS AND GRAVE
<Multi_key> <grave> <quotedbl> <U>		: "Ǜ"	U01DB # LATIN CAPITAL LETTER U WITH DIAERESIS AND GRAVE
<dead_grave> <udiaeresis>			: "ǜ"	U01DC # LATIN SMALL LETTER U WITH DIAERESIS AND GRAVE
<Multi_key> <grave> <udiaeresis>		: "ǜ"	U01DC # LATIN SMALL LETTER U WITH DIAERESIS AND GRAVE
<dead_grave> <dead_diaeresis> <u>		: "ǜ"	U01DC # LATIN SMALL LETTER U WITH DIAERESIS AND GRAVE
<dead_grave> <Multi_key> <quotedbl> <u>		: "ǜ"	U01DC # LATIN SMALL LETTER U WITH DIAERESIS AND GRAVE
<Multi_key> <grave> <dead_diaeresis> <u>	: "ǜ"	U01DC # LATIN SMALL LETTER U WITH DIAERESIS AND GRAVE
<Multi_key> <grave> <quotedbl> <u>		: "ǜ"	U01DC # LATIN SMALL LETTER U WITH DIAERESIS AND GRAVE
<dead_macron> <Adiaeresis>			: "Ǟ"	U01DE # LATIN CAPITAL LETTER A WITH DIAERESIS AND MACRON
<Multi_key> <macron> <Adiaeresis>		: "Ǟ"	U01DE # LATIN CAPITAL LETTER A WITH DIAERESIS AND MACRON
<Multi_key> <underscore> <Adiaeresis>		: "Ǟ"	U01DE # LATIN CAPITAL LETTER A WITH DIAERESIS AND MACRON
<dead_macron> <dead_diaeresis> <A>		: "Ǟ"	U01DE # LATIN CAPITAL LETTER A WITH DIAERESIS AND MACRON
<dead_macron> <Multi_key> <quotedbl> <A>	: "Ǟ"	U01DE # LATIN CAPITAL LETTER A WITH DIAERESIS AND MACRON
<Multi_key> <macron> <dead_diaeresis> <A>	: "Ǟ"	U01DE # LATIN CAPITAL LETTER A WITH DIAERESIS AND MACRON
<Multi_key> <macron> <quotedbl> <A>		: "Ǟ"	U01DE # LATIN CAPITAL LETTER A WITH DIAERESIS AND MACRON
<Multi_key> <underscore> <dead_diaeresis> <A>	: "Ǟ"	U01DE # LATIN CAPITAL LETTER A WITH DIAERESIS AND MACRON
<Multi_key> <underscore> <quotedbl> <A>		: "Ǟ"	U01DE # LATIN CAPITAL LETTER A WITH DIAERESIS AND MACRON
<dead_macron> <adiaeresis>			: "ǟ"	U01DF # LATIN SMALL LETTER A WITH DIAERESIS AND MACRON
<Multi_key> <macron> <adiaeresis>		: "ǟ"	U01DF # LATIN SMALL LETTER A WITH DIAERESIS AND MACRON
<Multi_key> <underscore> <adiaeresis>		: "ǟ"	U01DF # LATIN SMALL LETTER A WITH DIAERESIS AND MACRON
<dead_macron> <dead_diaeresis> <a>		: "ǟ"	U01DF # LATIN SMALL LETTER A WITH DIAERESIS AND MACRON
<dead_macron> <Multi_key> <quotedbl> <a>	: "ǟ"	U01DF # LATIN SMALL LETTER A WITH DIAERESIS AND MACRON
<Multi_key> <macron> <dead_diaeresis> <a>	: "ǟ"	U01DF # LATIN SMALL LETTER A WITH DIAERESIS AND MACRON
<Multi_key> <macron> <quotedbl> <a>		: "ǟ"	U01DF # LATIN SMALL LETTER A WITH DIAERESIS AND MACRON
<Multi_key> <underscore> <dead_diaeresis> <a>	: "ǟ"	U01DF # LATIN SMALL LETTER A WITH DIAERESIS AND MACRON
<Multi_key> <underscore> <quotedbl> <a>		: "ǟ"	U01DF # LATIN SMALL LETTER A WITH DIAERESIS AND MACRON
<dead_macron> <U0226>				: "Ǡ"	U01E0 # LATIN CAPITAL LETTER A WITH DOT ABOVE AND MACRON
<Multi_key> <macron> <U0226>			: "Ǡ"	U01E0 # LATIN CAPITAL LETTER A WITH DOT ABOVE AND MACRON
<Multi_key> <underscore> <U0226>		: "Ǡ"	U01E0 # LATIN CAPITAL LETTER A WITH DOT ABOVE AND MACRON
<dead_macron> <dead_abovedot> <A>		: "Ǡ"	U01E0 # LATIN CAPITAL LETTER A WITH DOT ABOVE AND MACRON
<dead_macron> <Multi_key> <period> <A>		: "Ǡ"	U01E0 # LATIN CAPITAL LETTER A WITH DOT ABOVE AND MACRON
<Multi_key> <macron> <dead_abovedot> <A>	: "Ǡ"	U01E0 # LATIN CAPITAL LETTER A WITH DOT ABOVE AND MACRON
<Multi_key> <macron> <period> <A>		: "Ǡ"	U01E0 # LATIN CAPITAL LETTER A WITH DOT ABOVE AND MACRON
<Multi_key> <underscore> <dead_abovedot> <A>	: "Ǡ"	U01E0 # LATIN CAPITAL LETTER A WITH DOT ABOVE AND MACRON
<Multi_key> <underscore> <period> <A>		: "Ǡ"	U01E0 # LATIN CAPITAL LETTER A WITH DOT ABOVE AND MACRON
<dead_macron> <U0227>				: "ǡ"	U01E1 # LATIN SMALL LETTER A WITH DOT ABOVE AND MACRON
<Multi_key> <macron> <U0227>			: "ǡ"	U01E1 # LATIN SMALL LETTER A WITH DOT ABOVE AND MACRON
<Multi_key> <underscore> <U0227>		: "ǡ"	U01E1 # LATIN SMALL LETTER A WITH DOT ABOVE AND MACRON
<dead_macron> <dead_abovedot> <a>		: "ǡ"	U01E1 # LATIN SMALL LETTER A WITH DOT ABOVE AND MACRON
<dead_macron> <Multi_key> <period> <a>		: "ǡ"	U01E1 # LATIN SMALL LETTER A WITH DOT ABOVE AND MACRON
<Multi_key> <macron> <dead_abovedot> <a>	: "ǡ"	U01E1 # LATIN SMALL LETTER A WITH DOT ABOVE AND MACRON
<Multi_key> <macron> <period> <a>		: "ǡ"	U01E1 # LATIN SMALL LETTER A WITH DOT ABOVE AND MACRON
<Multi_key> <underscore> <dead_abovedot> <a>	: "ǡ"	U01E1 # LATIN SMALL LETTER A WITH DOT ABOVE AND MACRON
<Multi_key> <underscore> <period> <a>		: "ǡ"	U01E1 # LATIN SMALL LETTER A WITH DOT ABOVE AND MACRON
<dead_macron> <AE>				: "Ǣ"	U01E2 # LATIN CAPITAL LETTER AE WITH MACRON
<Multi_key> <macron> <AE>			: "Ǣ"	U01E2 # LATIN CAPITAL LETTER AE WITH MACRON
<Multi_key> <underscore> <AE>			: "Ǣ"	U01E2 # LATIN CAPITAL LETTER AE WITH MACRON
<dead_macron> <ae>				: "ǣ"	U01E3 # LATIN SMALL LETTER AE WITH MACRON
<Multi_key> <macron> <ae>			: "ǣ"	U01E3 # LATIN SMALL LETTER AE WITH MACRON
<Multi_key> <underscore> <ae>			: "ǣ"	U01E3 # LATIN SMALL LETTER AE WITH MACRON
<dead_stroke> <G>				: "Ǥ"	U01E4 # LATIN CAPITAL LETTER G WITH STROKE
<Multi_key> <slash> <G>				: "Ǥ"	U01E4 # LATIN CAPITAL LETTER G WITH STROKE
<Multi_key> <KP_Divide> <G>			: "Ǥ"	U01E4 # LATIN CAPITAL LETTER G WITH STROKE
<dead_stroke> <g>				: "ǥ"	U01E5 # LATIN SMALL LETTER G WITH STROKE
<Multi_key> <slash> <g>				: "ǥ"	U01E5 # LATIN SMALL LETTER G WITH STROKE
<Multi_key> <KP_Divide> <g>			: "ǥ"	U01E5 # LATIN SMALL LETTER G WITH STROKE
<dead_caron> <G>				: "Ǧ"	U01E6 # LATIN CAPITAL LETTER G WITH CARON
<Multi_key> <c> <G>				: "Ǧ"	U01E6 # LATIN CAPITAL LETTER G WITH CARON
<Multi_key> <v> <G>				: "Ǧ"	U01E6 # LATIN CAPITAL LETTER G WITH CARON
<dead_caron> <g>				: "ǧ"	U01E7 # LATIN SMALL LETTER G WITH CARON
<Multi_key> <c> <g>				: "ǧ"	U01E7 # LATIN SMALL LETTER G WITH CARON
<Multi_key> <v> <g>				: "ǧ"	U01E7 # LATIN SMALL LETTER G WITH CARON
<dead_caron> <K>				: "Ǩ"	U01E8 # LATIN CAPITAL LETTER K WITH CARON
<Multi_key> <c> <K>				: "Ǩ"	U01E8 # LATIN CAPITAL LETTER K WITH CARON
<Multi_key> <v> <K>				: "Ǩ"	U01E8 # LATIN CAPITAL LETTER K WITH CARON
<dead_caron> <k>				: "ǩ"	U01E9 # LATIN SMALL LETTER K WITH CARON
<Multi_key> <c> <k>				: "ǩ"	U01E9 # LATIN SMALL LETTER K WITH CARON
<Multi_key> <v> <k>				: "ǩ"	U01E9 # LATIN SMALL LETTER K WITH CARON
<dead_ogonek> <O>				: "Ǫ"	U01EA # LATIN CAPITAL LETTER O WITH OGONEK
<Multi_key> <semicolon> <O>			: "Ǫ"	U01EA # LATIN CAPITAL LETTER O WITH OGONEK
<Multi_key> <O> <semicolon>			: "Ǫ"	U01EA # LATIN CAPITAL LETTER O WITH OGONEK
<Multi_key> <comma> <O>				: "Ǫ"	U01EA # LATIN CAPITAL LETTER O WITH OGONEK
<Multi_key> <O> <comma>				: "Ǫ"	U01EA # LATIN CAPITAL LETTER O WITH OGONEK
<dead_ogonek> <o>				: "ǫ"	U01EB # LATIN SMALL LETTER O WITH OGONEK
<Multi_key> <semicolon> <o>			: "ǫ"	U01EB # LATIN SMALL LETTER O WITH OGONEK
<Multi_key> <o> <semicolon>			: "ǫ"	U01EB # LATIN SMALL LETTER O WITH OGONEK
<Multi_key> <comma> <o>				: "ǫ"	U01EB # LATIN SMALL LETTER O WITH OGONEK
<Multi_key> <o> <comma>				: "ǫ"	U01EB # LATIN SMALL LETTER O WITH OGONEK
<dead_macron> <dead_ogonek> <O>			: "Ǭ"	U01EC # LATIN CAPITAL LETTER O WITH OGONEK AND MACRON
<dead_macron> <Multi_key> <semicolon> <O>	: "Ǭ"	U01EC # LATIN CAPITAL LETTER O WITH OGONEK AND MACRON
<Multi_key> <macron> <dead_ogonek> <O>		: "Ǭ"	U01EC # LATIN CAPITAL LETTER O WITH OGONEK AND MACRON
<Multi_key> <macron> <semicolon> <O>		: "Ǭ"	U01EC # LATIN CAPITAL LETTER O WITH OGONEK AND MACRON
<Multi_key> <underscore> <dead_ogonek> <O>	: "Ǭ"	U01EC # LATIN CAPITAL LETTER O WITH OGONEK AND MACRON
<Multi_key> <underscore> <semicolon> <O>	: "Ǭ"	U01EC # LATIN CAPITAL LETTER O WITH OGONEK AND MACRON
<dead_macron> <dead_ogonek> <o>			: "ǭ"	U01ED # LATIN SMALL LETTER O WITH OGONEK AND MACRON
<dead_macron> <Multi_key> <semicolon> <o>	: "ǭ"	U01ED # LATIN SMALL LETTER O WITH OGONEK AND MACRON
<Multi_key> <macron> <dead_ogonek> <o>		: "ǭ"	U01ED # LATIN SMALL LETTER O WITH OGONEK AND MACRON
<Multi_key> <macron> <semicolon> <o>		: "ǭ"	U01ED # LATIN SMALL LETTER O WITH OGONEK AND MACRON
<Multi_key> <underscore> <dead_ogonek> <o>	: "ǭ"	U01ED # LATIN SMALL LETTER O WITH OGONEK AND MACRON
<Multi_key> <underscore> <semicolon> <o>	: "ǭ"	U01ED # LATIN SMALL LETTER O WITH OGONEK AND MACRON
<dead_caron> <EZH>				: "Ǯ"	U01EE # LATIN CAPITAL LETTER EZH WITH CARON
<Multi_key> <c> <EZH>				: "Ǯ"	U01EE # LATIN CAPITAL LETTER EZH WITH CARON
<Multi_key> <v> <EZH>				: "Ǯ"	U01EE # LATIN CAPITAL LETTER EZH WITH CARON
<dead_caron> <ezh>				: "ǯ"	U01EF # LATIN SMALL LETTER EZH WITH CARON
<Multi_key> <c> <ezh>				: "ǯ"	U01EF # LATIN SMALL LETTER EZH WITH CARON
<Multi_key> <v> <ezh>				: "ǯ"	U01EF # LATIN SMALL LETTER EZH WITH CARON
<dead_caron> <j>				: "ǰ"	U01F0 # LATIN SMALL LETTER J WITH CARON
<Multi_key> <c> <j>				: "ǰ"	U01F0 # LATIN SMALL LETTER J WITH CARON
<Multi_key> <v> <j>				: "ǰ"	U01F0 # LATIN SMALL LETTER J WITH CARON
<dead_acute> <G>				: "Ǵ"	U01F4 # LATIN CAPITAL LETTER G WITH ACUTE
<Multi_key> <acute> <G>				: "Ǵ"	U01F4 # LATIN CAPITAL LETTER G WITH ACUTE
<Multi_key> <apostrophe> <G>			: "Ǵ"	U01F4 # LATIN CAPITAL LETTER G WITH ACUTE
<dead_acute> <g>				: "ǵ"	U01F5 # LATIN SMALL LETTER G WITH ACUTE
<Multi_key> <acute> <g>				: "ǵ"	U01F5 # LATIN SMALL LETTER G WITH ACUTE
<Multi_key> <apostrophe> <g>			: "ǵ"	U01F5 # LATIN SMALL LETTER G WITH ACUTE
<dead_grave> <N>				: "Ǹ"	U01F8 # LATIN CAPITAL LETTER N WITH GRAVE
<Multi_key> <grave> <N>				: "Ǹ"	U01F8 # LATIN CAPITAL LETTER N WITH GRAVE
<dead_grave> <n>				: "ǹ"	U01F9 # LATIN SMALL LETTER N WITH GRAVE
<Multi_key> <grave> <n>				: "ǹ"	U01F9 # LATIN SMALL LETTER N WITH GRAVE
<dead_acute> <Aring>				: "Ǻ"	U01FA # LATIN CAPITAL LETTER A WITH RING ABOVE AND ACUTE
<Multi_key> <acute> <Aring>			: "Ǻ"	U01FA # LATIN CAPITAL LETTER A WITH RING ABOVE AND ACUTE
<Multi_key> <apostrophe> <Aring>		: "Ǻ"	U01FA # LATIN CAPITAL LETTER A WITH RING ABOVE AND ACUTE
<dead_acute> <dead_abovering> <A>		: "Ǻ"	U01FA # LATIN CAPITAL LETTER A WITH RING ABOVE AND ACUTE
<dead_acute> <Multi_key> <o> <A>		: "Ǻ"	U01FA # LATIN CAPITAL LETTER A WITH RING ABOVE AND ACUTE
<Multi_key> <acute> <dead_abovering> <A>	: "Ǻ"	U01FA # LATIN CAPITAL LETTER A WITH RING ABOVE AND ACUTE
<Multi_key> <apostrophe> <dead_abovering> <A>	: "Ǻ"	U01FA # LATIN CAPITAL LETTER A WITH RING ABOVE AND ACUTE
<Multi_key> <asterisk> <apostrophe> <A>		: "Ǻ"	U01FA # LATIN CAPITAL LETTER A WITH RING ABOVE AND ACUTE
<dead_acute> <aring>				: "ǻ"	U01FB # LATIN SMALL LETTER A WITH RING ABOVE AND ACUTE
<Multi_key> <acute> <aring>			: "ǻ"	U01FB # LATIN SMALL LETTER A WITH RING ABOVE AND ACUTE
<Multi_key> <apostrophe> <aring>		: "ǻ"	U01FB # LATIN SMALL LETTER A WITH RING ABOVE AND ACUTE
<dead_acute> <dead_abovering> <a>		: "ǻ"	U01FB # LATIN SMALL LETTER A WITH RING ABOVE AND ACUTE
<dead_acute> <Multi_key> <o> <a>		: "ǻ"	U01FB # LATIN SMALL LETTER A WITH RING ABOVE AND ACUTE
<Multi_key> <acute> <dead_abovering> <a>	: "ǻ"	U01FB # LATIN SMALL LETTER A WITH RING ABOVE AND ACUTE
<Multi_key> <apostrophe> <dead_abovering> <a>	: "ǻ"	U01FB # LATIN SMALL LETTER A WITH RING ABOVE AND ACUTE
<Multi_key> <asterisk> <apostrophe> <a>		: "ǻ"	U01FB # LATIN SMALL LETTER A WITH RING ABOVE AND ACUTE
<dead_acute> <AE>				: "Ǽ"	U01FC # LATIN CAPITAL LETTER AE WITH ACUTE
<Multi_key> <acute> <AE>			: "Ǽ"	U01FC # LATIN CAPITAL LETTER AE WITH ACUTE
<Multi_key> <apostrophe> <AE>			: "Ǽ"	U01FC # LATIN CAPITAL LETTER AE WITH ACUTE
<dead_acute> <ae>				: "ǽ"	U01FD # LATIN SMALL LETTER AE WITH ACUTE
<Multi_key> <acute> <ae>			: "ǽ"	U01FD # LATIN SMALL LETTER AE WITH ACUTE
<Multi_key> <apostrophe> <ae>			: "ǽ"	U01FD # LATIN SMALL LETTER AE WITH ACUTE
<dead_acute> <Ooblique>				: "Ǿ"	U01FE # LATIN CAPITAL LETTER O WITH STROKE AND ACUTE
<Multi_key> <acute> <Ooblique>			: "Ǿ"	U01FE # LATIN CAPITAL LETTER O WITH STROKE AND ACUTE
<Multi_key> <apostrophe> <Ooblique>		: "Ǿ"	U01FE # LATIN CAPITAL LETTER O WITH STROKE AND ACUTE
<dead_acute> <dead_stroke> <O>			: "Ǿ"	U01FE # LATIN CAPITAL LETTER O WITH STROKE AND ACUTE
<dead_acute> <Multi_key> <slash> <O>		: "Ǿ"	U01FE # LATIN CAPITAL LETTER O WITH STROKE AND ACUTE
<Multi_key> <acute> <slash> <O>			: "Ǿ"	U01FE # LATIN CAPITAL LETTER O WITH STROKE AND ACUTE
<Multi_key> <apostrophe> <slash> <O>		: "Ǿ"	U01FE # LATIN CAPITAL LETTER O WITH STROKE AND ACUTE
<dead_acute> <Multi_key> <KP_Divide> <O>	: "Ǿ"	U01FE # LATIN CAPITAL LETTER O WITH STROKE AND ACUTE
<Multi_key> <acute> <KP_Divide> <O>		: "Ǿ"	U01FE # LATIN CAPITAL LETTER O WITH STROKE AND ACUTE
<Multi_key> <apostrophe> <KP_Divide> <O>	: "Ǿ"	U01FE # LATIN CAPITAL LETTER O WITH STROKE AND ACUTE
<dead_stroke> <dead_acute> <O>			: "Ǿ"	U01FE # LATIN CAPITAL LETTER O WITH STROKE AND ACUTE
<dead_acute> <oslash>				: "ǿ"	U01FF # LATIN SMALL LETTER O WITH STROKE AND ACUTE
<Multi_key> <acute> <oslash>			: "ǿ"	U01FF # LATIN SMALL LETTER O WITH STROKE AND ACUTE
<Multi_key> <apostrophe> <oslash>		: "ǿ"	U01FF # LATIN SMALL LETTER O WITH STROKE AND ACUTE
<dead_acute> <dead_stroke> <o>			: "ǿ"	U01FF # LATIN SMALL LETTER O WITH STROKE AND ACUTE
<dead_acute> <Multi_key> <slash> <o>		: "ǿ"	U01FF # LATIN SMALL LETTER O WITH STROKE AND ACUTE
<Multi_key> <acute> <slash> <o>			: "ǿ"	U01FF # LATIN SMALL LETTER O WITH STROKE AND ACUTE
<Multi_key> <apostrophe> <slash> <o>		: "ǿ"	U01FF # LATIN SMALL LETTER O WITH STROKE AND ACUTE
<dead_acute> <Multi_key> <KP_Divide> <o>	: "ǿ"	U01FF # LATIN SMALL LETTER O WITH STROKE AND ACUTE
<Multi_key> <acute> <KP_Divide> <o>		: "ǿ"	U01FF # LATIN SMALL LETTER O WITH STROKE AND ACUTE
<Multi_key> <apostrophe> <KP_Divide> <o>	: "ǿ"	U01FF # LATIN SMALL LETTER O WITH STROKE AND ACUTE
<dead_stroke> <dead_acute> <o>			: "ǿ"	U01FF # LATIN SMALL LETTER O WITH STROKE AND ACUTE
<dead_doublegrave> <A>				: "Ȁ"	U0200 # LATIN CAPITAL LETTER A WITH DOUBLE GRAVE
<dead_doublegrave> <a>				: "ȁ"	U0201 # LATIN SMALL LETTER A WITH DOUBLE GRAVE
<dead_invertedbreve> <A>			: "Ȃ"	U0202 # LATIN CAPITAL LETTER A WITH INVERTED BREVE
<dead_invertedbreve> <a>			: "ȃ"	U0203 # LATIN SMALL LETTER A WITH INVERTED BREVE
<dead_doublegrave> <E>				: "Ȅ"	U0204 # LATIN CAPITAL LETTER E WITH DOUBLE GRAVE
<dead_doublegrave> <e>				: "ȅ"	U0205 # LATIN SMALL LETTER E WITH DOUBLE GRAVE
<dead_invertedbreve> <E>			: "Ȇ"	U0206 # LATIN CAPITAL LETTER E WITH INVERTED BREVE
<dead_invertedbreve> <e>			: "ȇ"	U0207 # LATIN SMALL LETTER E WITH INVERTED BREVE
<dead_doublegrave> <I>				: "Ȉ"	U0208 # LATIN CAPITAL LETTER I WITH DOUBLE GRAVE
<dead_doublegrave> <i>				: "ȉ"	U0209 # LATIN SMALL LETTER I WITH DOUBLE GRAVE
<dead_invertedbreve> <I>			: "Ȋ"	U020A # LATIN CAPITAL LETTER I WITH INVERTED BREVE
<dead_invertedbreve> <i>			: "ȋ"	U020B # LATIN SMALL LETTER I WITH INVERTED BREVE
<dead_doublegrave> <O>				: "Ȍ"	U020C # LATIN CAPITAL LETTER O WITH DOUBLE GRAVE
<dead_doublegrave> <o>				: "ȍ"	U020D # LATIN SMALL LETTER O WITH DOUBLE GRAVE
<dead_invertedbreve> <O>			: "Ȏ"	U020E # LATIN CAPITAL LETTER O WITH INVERTED BREVE
<dead_invertedbreve> <o>			: "ȏ"	U020F # LATIN SMALL LETTER O WITH INVERTED BREVE
<dead_doublegrave> <R>				: "Ȑ"	U0210 # LATIN CAPITAL LETTER R WITH DOUBLE GRAVE
<dead_doublegrave> <r>				: "ȑ"	U0211 # LATIN SMALL LETTER R WITH DOUBLE GRAVE
<dead_invertedbreve> <R>			: "Ȓ"	U0212 # LATIN CAPITAL LETTER R WITH INVERTED BREVE
<dead_invertedbreve> <r>			: "ȓ"	U0213 # LATIN SMALL LETTER R WITH INVERTED BREVE
<dead_doublegrave> <U>				: "Ȕ"	U0214 # LATIN CAPITAL LETTER U WITH DOUBLE GRAVE
<dead_doublegrave> <u>				: "ȕ"	U0215 # LATIN SMALL LETTER U WITH DOUBLE GRAVE
<dead_invertedbreve> <U>			: "Ȗ"	U0216 # LATIN CAPITAL LETTER U WITH INVERTED BREVE
<dead_invertedbreve> <u>			: "ȗ"	U0217 # LATIN SMALL LETTER U WITH INVERTED BREVE
<dead_belowcomma> <S>				: "Ș"	U0218 # LATIN CAPITAL LETTER S WITH COMMA BELOW
<Multi_key> <semicolon> <S>			: "Ș"	U0218 # LATIN CAPITAL LETTER S WITH COMMA BELOW
<Multi_key> <S> <semicolon>			: "Ș"	U0218 # LATIN CAPITAL LETTER S WITH COMMA BELOW
<dead_belowcomma> <s>				: "ș"	U0219 # LATIN SMALL LETTER S WITH COMMA BELOW
<Multi_key> <semicolon> <s>			: "ș"	U0219 # LATIN SMALL LETTER S WITH COMMA BELOW
<Multi_key> <s> <semicolon>			: "ș"	U0219 # LATIN SMALL LETTER S WITH COMMA BELOW
<dead_belowcomma> <T>				: "Ț"	U021A # LATIN CAPITAL LETTER T WITH COMMA BELOW
<Multi_key> <semicolon> <T>			: "Ț"	U021A # LATIN CAPITAL LETTER T WITH COMMA BELOW
<Multi_key> <T> <semicolon>			: "Ț"	U021A # LATIN CAPITAL LETTER T WITH COMMA BELOW
<dead_belowcomma> <t>				: "ț"	U021B # LATIN SMALL LETTER T WITH COMMA BELOW
<Multi_key> <semicolon> <t>			: "ț"	U021B # LATIN SMALL LETTER T WITH COMMA BELOW
<Multi_key> <t> <semicolon>			: "ț"	U021B # LATIN SMALL LETTER T WITH COMMA BELOW
<dead_caron> <H>				: "Ȟ"	U021E # LATIN CAPITAL LETTER H WITH CARON
<Multi_key> <c> <H>				: "Ȟ"	U021E # LATIN CAPITAL LETTER H WITH CARON
<Multi_key> <v> <H>				: "Ȟ"	U021E # LATIN CAPITAL LETTER H WITH CARON
<dead_caron> <h>				: "ȟ"	U021F # LATIN SMALL LETTER H WITH CARON
<Multi_key> <c> <h>				: "ȟ"	U021F # LATIN SMALL LETTER H WITH CARON
<Multi_key> <v> <h>				: "ȟ"	U021F # LATIN SMALL LETTER H WITH CARON
<dead_abovedot> <A>				: "Ȧ"	U0226 # LATIN CAPITAL LETTER A WITH DOT ABOVE
<Multi_key> <period> <A>			: "Ȧ"	U0226 # LATIN CAPITAL LETTER A WITH DOT ABOVE
<dead_abovedot> <a>				: "ȧ"	U0227 # LATIN SMALL LETTER A WITH DOT ABOVE
<Multi_key> <period> <a>			: "ȧ"	U0227 # LATIN SMALL LETTER A WITH DOT ABOVE
<dead_cedilla> <E>				: "Ȩ"	U0228 # LATIN CAPITAL LETTER E WITH CEDILLA
<Multi_key> <cedilla> <E>			: "Ȩ"	U0228 # LATIN CAPITAL LETTER E WITH CEDILLA
<dead_cedilla> <e>				: "ȩ"	U0229 # LATIN SMALL LETTER E WITH CEDILLA
<Multi_key> <cedilla> <e>			: "ȩ"	U0229 # LATIN SMALL LETTER E WITH CEDILLA
<dead_macron> <Odiaeresis>			: "Ȫ"	U022A # LATIN CAPITAL LETTER O WITH DIAERESIS AND MACRON
<Multi_key> <macron> <Odiaeresis>		: "Ȫ"	U022A # LATIN CAPITAL LETTER O WITH DIAERESIS AND MACRON
<Multi_key> <underscore> <Odiaeresis>		: "Ȫ"	U022A # LATIN CAPITAL LETTER O WITH DIAERESIS AND MACRON
<dead_macron> <dead_diaeresis> <O>		: "Ȫ"	U022A # LATIN CAPITAL LETTER O WITH DIAERESIS AND MACRON
<dead_macron> <Multi_key> <quotedbl> <O>	: "Ȫ"	U022A # LATIN CAPITAL LETTER O WITH DIAERESIS AND MACRON
<Multi_key> <macron> <dead_diaeresis> <O>	: "Ȫ"	U022A # LATIN CAPITAL LETTER O WITH DIAERESIS AND MACRON
<Multi_key> <macron> <quotedbl> <O>		: "Ȫ"	U022A # LATIN CAPITAL LETTER O WITH DIAERESIS AND MACRON
<Multi_key> <underscore> <dead_diaeresis> <O>	: "Ȫ"	U022A # LATIN CAPITAL LETTER O WITH DIAERESIS AND MACRON
<Multi_key> <underscore> <quotedbl> <O>		: "Ȫ"	U022A # LATIN CAPITAL LETTER O WITH DIAERESIS AND MACRON
<dead_macron> <odiaeresis>			: "ȫ"	U022B # LATIN SMALL LETTER O WITH DIAERESIS AND MACRON
<Multi_key> <macron> <odiaeresis>		: "ȫ"	U022B # LATIN SMALL LETTER O WITH DIAERESIS AND MACRON
<Multi_key> <underscore> <odiaeresis>		: "ȫ"	U022B # LATIN SMALL LETTER O WITH DIAERESIS AND MACRON
<dead_macron> <dead_diaeresis> <o>		: "ȫ"	U022B # LATIN SMALL LETTER O WITH DIAERESIS AND MACRON
<dead_macron> <Multi_key> <quotedbl> <o>	: "ȫ"	U022B # LATIN SMALL LETTER O WITH DIAERESIS AND MACRON
<Multi_key> <macron> <dead_diaeresis> <o>	: "ȫ"	U022B # LATIN SMALL LETTER O WITH DIAERESIS AND MACRON
<Multi_key> <macron> <quotedbl> <o>		: "ȫ"	U022B # LATIN SMALL LETTER O WITH DIAERESIS AND MACRON
<Multi_key> <underscore> <dead_diaeresis> <o>	: "ȫ"	U022B # LATIN SMALL LETTER O WITH DIAERESIS AND MACRON
<Multi_key> <underscore> <quotedbl> <o>		: "ȫ"	U022B # LATIN SMALL LETTER O WITH DIAERESIS AND MACRON
<dead_macron> <Otilde>				: "Ȭ"	U022C # LATIN CAPITAL LETTER O WITH TILDE AND MACRON
<Multi_key> <macron> <Otilde>			: "Ȭ"	U022C # LATIN CAPITAL LETTER O WITH TILDE AND MACRON
<Multi_key> <underscore> <Otilde>		: "Ȭ"	U022C # LATIN CAPITAL LETTER O WITH TILDE AND MACRON
<dead_macron> <dead_tilde> <O>			: "Ȭ"	U022C # LATIN CAPITAL LETTER O WITH TILDE AND MACRON
<dead_macron> <Multi_key> <asciitilde> <O>	: "Ȭ"	U022C # LATIN CAPITAL LETTER O WITH TILDE AND MACRON
<Multi_key> <macron> <dead_tilde> <O>		: "Ȭ"	U022C # LATIN CAPITAL LETTER O WITH TILDE AND MACRON
<Multi_key> <macron> <asciitilde> <O>		: "Ȭ"	U022C # LATIN CAPITAL LETTER O WITH TILDE AND MACRON
<Multi_key> <underscore> <dead_tilde> <O>	: "Ȭ"	U022C # LATIN CAPITAL LETTER O WITH TILDE AND MACRON
<Multi_key> <underscore> <asciitilde> <O>	: "Ȭ"	U022C # LATIN CAPITAL LETTER O WITH TILDE AND MACRON
<dead_macron> <otilde>				: "ȭ"	U022D # LATIN SMALL LETTER O WITH TILDE AND MACRON
<Multi_key> <macron> <otilde>			: "ȭ"	U022D # LATIN SMALL LETTER O WITH TILDE AND MACRON
<Multi_key> <underscore> <otilde>		: "ȭ"	U022D # LATIN SMALL LETTER O WITH TILDE AND MACRON
<dead_macron> <dead_tilde> <o>			: "ȭ"	U022D # LATIN SMALL LETTER O WITH TILDE AND MACRON
<dead_macron> <Multi_key> <asciitilde> <o>	: "ȭ"	U022D # LATIN SMALL LETTER O WITH TILDE AND MACRON
<Multi_key> <macron> <dead_tilde> <o>		: "ȭ"	U022D # LATIN SMALL LETTER O WITH TILDE AND MACRON
<Multi_key> <macron> <asciitilde> <o>		: "ȭ"	U022D # LATIN SMALL LETTER O WITH TILDE AND MACRON
<Multi_key> <underscore> <dead_tilde> <o>	: "ȭ"	U022D # LATIN SMALL LETTER O WITH TILDE AND MACRON
<Multi_key> <underscore> <asciitilde> <o>	: "ȭ"	U022D # LATIN SMALL LETTER O WITH TILDE AND MACRON
<dead_abovedot> <O>				: "Ȯ"	U022E # LATIN CAPITAL LETTER O WITH DOT ABOVE
<Multi_key> <period> <O>			: "Ȯ"	U022E # LATIN CAPITAL LETTER O WITH DOT ABOVE
<dead_abovedot> <o>				: "ȯ"	U022F # LATIN SMALL LETTER O WITH DOT ABOVE
<Multi_key> <period> <o>			: "ȯ"	U022F # LATIN SMALL LETTER O WITH DOT ABOVE
<dead_macron> <dead_abovedot> <O>		: "Ȱ"	U0230 # LATIN CAPITAL LETTER O WITH DOT ABOVE AND MACRON
<dead_macron> <Multi_key> <period> <O>		: "Ȱ"	U0230 # LATIN CAPITAL LETTER O WITH DOT ABOVE AND MACRON
<Multi_key> <macron> <dead_abovedot> <O>	: "Ȱ"	U0230 # LATIN CAPITAL LETTER O WITH DOT ABOVE AND MACRON
<Multi_key> <macron> <period> <O>		: "Ȱ"	U0230 # LATIN CAPITAL LETTER O WITH DOT ABOVE AND MACRON
<Multi_key> <underscore> <dead_abovedot> <O>	: "Ȱ"	U0230 # LATIN CAPITAL LETTER O WITH DOT ABOVE AND MACRON
<Multi_key> <underscore> <period> <O>		: "Ȱ"	U0230 # LATIN CAPITAL LETTER O WITH DOT ABOVE AND MACRON
<dead_macron> <dead_abovedot> <o>		: "ȱ"	U0231 # LATIN SMALL LETTER O WITH DOT ABOVE AND MACRON
<dead_macron> <Multi_key> <period> <o>		: "ȱ"	U0231 # LATIN SMALL LETTER O WITH DOT ABOVE AND MACRON
<Multi_key> <macron> <dead_abovedot> <o>	: "ȱ"	U0231 # LATIN SMALL LETTER O WITH DOT ABOVE AND MACRON
<Multi_key> <macron> <period> <o>		: "ȱ"	U0231 # LATIN SMALL LETTER O WITH DOT ABOVE AND MACRON
<Multi_key> <underscore> <dead_abovedot> <o>	: "ȱ"	U0231 # LATIN SMALL LETTER O WITH DOT ABOVE AND MACRON
<Multi_key> <underscore> <period> <o>		: "ȱ"	U0231 # LATIN SMALL LETTER O WITH DOT ABOVE AND MACRON
<dead_macron> <Y>				: "Ȳ"	U0232 # LATIN CAPITAL LETTER Y WITH MACRON
<Multi_key> <macron> <Y>			: "Ȳ"	U0232 # LATIN CAPITAL LETTER Y WITH MACRON
<Multi_key> <underscore> <Y>			: "Ȳ"	U0232 # LATIN CAPITAL LETTER Y WITH MACRON
<dead_macron> <y>				: "ȳ"	U0233 # LATIN SMALL LETTER Y WITH MACRON
<Multi_key> <macron> <y>			: "ȳ"	U0233 # LATIN SMALL LETTER Y WITH MACRON
<Multi_key> <underscore> <y>			: "ȳ"	U0233 # LATIN SMALL LETTER Y WITH MACRON
<dead_stroke> <B>				: "Ƀ"	U0243 # LATIN CAPITAL LETTER B WITH STROKE
<Multi_key> <slash> <B>				: "Ƀ"	U0243 # LATIN CAPITAL LETTER B WITH STROKE
<Multi_key> <KP_Divide> <B>			: "Ƀ"	U0243 # LATIN CAPITAL LETTER B WITH STROKE
<Multi_key> <minus> <period> <E>		: "Ė̄"	# LATIN CAPITAL LETTER E WITH DOT ABOVE plus combining macron
<Multi_key> <underscore> <period> <E>		: "Ė̄"	# LATIN CAPITAL LETTER E WITH DOT ABOVE plus combining macron
<Multi_key> <minus> <period> <e>		: "ė̄"	# LATIN SMALL LETTER E WITH DOT ABOVE plus combining macron
<Multi_key> <underscore> <period> <e>		: "ė̄"	# LATIN SMALL LETTER E WITH DOT ABOVE plus combining macron
# IPA Extensions
<Multi_key> <e> <e>				: "ə"	U0259 # LATIN SMALL LETTER SCHWA
<dead_stroke> <i>				: "ɨ"	U0268 # LATIN SMALL LETTER I WITH STROKE
<Multi_key> <slash> <i>				: "ɨ"	U0268 # LATIN SMALL LETTER I WITH STROKE
<Multi_key> <KP_Divide> <i>			: "ɨ"	U0268 # LATIN SMALL LETTER I WITH STROKE
# Spacing Modifier Letters
<Multi_key> <slash> <U0294>				: "ʡ"	U02A1 # LATIN LETTER GLOTTAL STOP WITH STROKE
<Multi_key> <KP_Divide> <U0294>				: "ʡ"	U02A1 # LATIN LETTER GLOTTAL STOP WITH STROKE
<dead_circumflex> <Multi_key> <underscore> <h>		: "ʰ"	U02B0 # MODIFIER LETTER SMALL H
<Multi_key> <asciicircum> <underscore> <h>		: "ʰ"	U02B0 # MODIFIER LETTER SMALL H
<dead_circumflex> <Multi_key> <underscore> <U0266>	: "ʱ"	U02B1 # MODIFIER LETTER SMALL H WITH HOOK
<Multi_key> <asciicircum> <underscore> <U0266>		: "ʱ"	U02B1 # MODIFIER LETTER SMALL H WITH HOOK
<dead_circumflex> <Multi_key> <underscore> <j>		: "ʲ"	U02B2 # MODIFIER LETTER SMALL J
<Multi_key> <asciicircum> <underscore> <j>		: "ʲ"	U02B2 # MODIFIER LETTER SMALL J
<dead_circumflex> <Multi_key> <underscore> <r>		: "ʳ"	U02B3 # MODIFIER LETTER SMALL R
<Multi_key> <asciicircum> <underscore> <r>		: "ʳ"	U02B3 # MODIFIER LETTER SMALL R
<dead_circumflex> <Multi_key> <underscore> <U0279>	: "ʴ"	U02B4 # MODIFIER LETTER SMALL TURNED R
<Multi_key> <asciicircum> <underscore> <U0279>		: "ʴ"	U02B4 # MODIFIER LETTER SMALL TURNED R
<dead_circumflex> <Multi_key> <underscore> <U027B>	: "ʵ"	U02B5 # MODIFIER LETTER SMALL TURNED R WITH HOOK
<Multi_key> <asciicircum> <underscore> <U027B>		: "ʵ"	U02B5 # MODIFIER LETTER SMALL TURNED R WITH HOOK
<dead_circumflex> <Multi_key> <underscore> <U0281>	: "ʶ"	U02B6 # MODIFIER LETTER SMALL CAPITAL INVERTED R
<Multi_key> <asciicircum> <underscore> <U0281>		: "ʶ"	U02B6 # MODIFIER LETTER SMALL CAPITAL INVERTED R
<dead_circumflex> <Multi_key> <underscore> <w>		: "ʷ"	U02B7 # MODIFIER LETTER SMALL W
<Multi_key> <asciicircum> <underscore> <w>		: "ʷ"	U02B7 # MODIFIER LETTER SMALL W
<dead_circumflex> <Multi_key> <underscore> <y>		: "ʸ"	U02B8 # MODIFIER LETTER SMALL Y
<Multi_key> <asciicircum> <underscore> <y>		: "ʸ"	U02B8 # MODIFIER LETTER SMALL Y
<dead_circumflex> <Multi_key> <underscore> <U0263>	: "ˠ"	U02E0 # MODIFIER LETTER SMALL GAMMA
<Multi_key> <asciicircum> <underscore> <U0263>		: "ˠ"	U02E0 # MODIFIER LETTER SMALL GAMMA
<dead_circumflex> <Multi_key> <underscore> <l>		: "ˡ"	U02E1 # MODIFIER LETTER SMALL L
<Multi_key> <asciicircum> <underscore> <l>		: "ˡ"	U02E1 # MODIFIER LETTER SMALL L
<dead_circumflex> <Multi_key> <underscore> <s>		: "ˢ"	U02E2 # MODIFIER LETTER SMALL S
<Multi_key> <asciicircum> <underscore> <s>		: "ˢ"	U02E2 # MODIFIER LETTER SMALL S
<dead_circumflex> <Multi_key> <underscore> <x>		: "ˣ"	U02E3 # MODIFIER LETTER SMALL X
<Multi_key> <asciicircum> <underscore> <x>		: "ˣ"	U02E3 # MODIFIER LETTER SMALL X
<dead_circumflex> <Multi_key> <underscore> <U0295>	: "ˤ"	U02E4 # MODIFIER LETTER SMALL REVERSED GLOTTAL STOP
<Multi_key> <asciicircum> <underscore> <U0295>		: "ˤ"	U02E4 # MODIFIER LETTER SMALL REVERSED GLOTTAL STOP
# Greek
<dead_diaeresis> <acute>				: "̈́"	U0344 # COMBINING GREEK DIALYTIKA TONOS
<dead_diaeresis> <apostrophe>				: "̈́"	U0344 # COMBINING GREEK DIALYTIKA TONOS
<Multi_key> <quotedbl> <dead_acute>			: "̈́"	U0344 # COMBINING GREEK DIALYTIKA TONOS
<Multi_key> <quotedbl> <acute>				: "̈́"	U0344 # COMBINING GREEK DIALYTIKA TONOS
<Multi_key> <quotedbl> <apostrophe>			: "̈́"	U0344 # COMBINING GREEK DIALYTIKA TONOS
<dead_acute> <dead_diaeresis> <space>			: "΅"	U0385 # GREEK DIALYTIKA TONOS
<dead_diaeresis> <dead_acute> <space>			: "΅"	U0385 # GREEK DIALYTIKA TONOS
<Multi_key> <diaeresis> <dead_acute>			: "΅"	U0385 # GREEK DIALYTIKA TONOS
<Multi_key> <diaeresis> <acute>				: "΅"	U0385 # GREEK DIALYTIKA TONOS
<Multi_key> <diaeresis> <apostrophe>			: "΅"	U0385 # GREEK DIALYTIKA TONOS
<Multi_key> <apostrophe> <quotedbl> <space>		: "΅"	U0385 # GREEK DIALYTIKA TONOS
<dead_acute> <Greek_ALPHA>				: "Ά"	U0386 # GREEK CAPITAL LETTER ALPHA WITH TONOS
<Multi_key> <acute> <Greek_ALPHA>			: "Ά"	U0386 # GREEK CAPITAL LETTER ALPHA WITH TONOS
<Multi_key> <apostrophe> <Greek_ALPHA>			: "Ά"	U0386 # GREEK CAPITAL LETTER ALPHA WITH TONOS
<Multi_key> <Greek_ALPHA> <apostrophe>			: "Ά"	U0386 # GREEK CAPITAL LETTER ALPHA WITH TONOS
<dead_acute> <Greek_EPSILON>				: "Έ"	U0388 # GREEK CAPITAL LETTER EPSILON WITH TONOS
<Multi_key> <acute> <Greek_EPSILON>			: "Έ"	U0388 # GREEK CAPITAL LETTER EPSILON WITH TONOS
<Multi_key> <apostrophe> <Greek_EPSILON>		: "Έ"	U0388 # GREEK CAPITAL LETTER EPSILON WITH TONOS
<Multi_key> <Greek_EPSILON> <apostrophe>		: "Έ"	U0388 # GREEK CAPITAL LETTER EPSILON WITH TONOS
<dead_acute> <Greek_ETA>				: "Ή"	U0389 # GREEK CAPITAL LETTER ETA WITH TONOS
<Multi_key> <acute> <Greek_ETA>				: "Ή"	U0389 # GREEK CAPITAL LETTER ETA WITH TONOS
<Multi_key> <apostrophe> <Greek_ETA>			: "Ή"	U0389 # GREEK CAPITAL LETTER ETA WITH TONOS
<Multi_key> <Greek_ETA> <apostrophe>			: "Ή"	U0389 # GREEK CAPITAL LETTER ETA WITH TONOS
<dead_acute> <Greek_IOTA>				: "Ί"	U038A # GREEK CAPITAL LETTER IOTA WITH TONOS
<Multi_key> <acute> <Greek_IOTA>			: "Ί"	U038A # GREEK CAPITAL LETTER IOTA WITH TONOS
<Multi_key> <apostrophe> <Greek_IOTA>			: "Ί"	U038A # GREEK CAPITAL LETTER IOTA WITH TONOS
<Multi_key> <Greek_IOTA> <apostrophe>			: "Ί"	U038A # GREEK CAPITAL LETTER IOTA WITH TONOS
<dead_acute> <Greek_OMICRON>				: "Ό"	U038C # GREEK CAPITAL LETTER OMICRON WITH TONOS
<Multi_key> <acute> <Greek_OMICRON>			: "Ό"	U038C # GREEK CAPITAL LETTER OMICRON WITH TONOS
<Multi_key> <apostrophe> <Greek_OMICRON>		: "Ό"	U038C # GREEK CAPITAL LETTER OMICRON WITH TONOS
<Multi_key> <Greek_OMICRON> <apostrophe>		: "Ό"	U038C # GREEK CAPITAL LETTER OMICRON WITH TONOS
<dead_acute> <Greek_UPSILON>				: "Ύ"	U038E # GREEK CAPITAL LETTER UPSILON WITH TONOS
<Multi_key> <acute> <Greek_UPSILON>			: "Ύ"	U038E # GREEK CAPITAL LETTER UPSILON WITH TONOS
<Multi_key> <apostrophe> <Greek_UPSILON>		: "Ύ"	U038E # GREEK CAPITAL LETTER UPSILON WITH TONOS
<Multi_key> <Greek_UPSILON> <apostrophe>		: "Ύ"	U038E # GREEK CAPITAL LETTER UPSILON WITH TONOS
<dead_acute> <Greek_OMEGA>				: "Ώ"	U038F # GREEK CAPITAL LETTER OMEGA WITH TONOS
<Multi_key> <acute> <Greek_OMEGA>			: "Ώ"	U038F # GREEK CAPITAL LETTER OMEGA WITH TONOS
<Multi_key> <apostrophe> <Greek_OMEGA>			: "Ώ"	U038F # GREEK CAPITAL LETTER OMEGA WITH TONOS
<Multi_key> <Greek_OMEGA> <apostrophe>			: "Ώ"	U038F # GREEK CAPITAL LETTER OMEGA WITH TONOS
<dead_acute> <dead_diaeresis> <Greek_iota>		: "ΐ"	U0390 # GREEK SMALL LETTER IOTA WITH DIALYTIKA AND TONOS
<dead_diaeresis> <dead_acute> <Greek_iota>		: "ΐ"	U0390 # GREEK SMALL LETTER IOTA WITH DIALYTIKA AND TONOS
<dead_acute> <Multi_key> <quotedbl> <Greek_iota>	: "ΐ"	U0390 # GREEK SMALL LETTER IOTA WITH DIALYTIKA AND TONOS
<Multi_key> <acute> <dead_diaeresis> <Greek_iota>	: "ΐ"	U0390 # GREEK SMALL LETTER IOTA WITH DIALYTIKA AND TONOS
<Multi_key> <acute> <quotedbl> <Greek_iota>		: "ΐ"	U0390 # GREEK SMALL LETTER IOTA WITH DIALYTIKA AND TONOS
<Multi_key> <apostrophe> <dead_diaeresis> <Greek_iota>	: "ΐ"	U0390 # GREEK SMALL LETTER IOTA WITH DIALYTIKA AND TONOS
<Multi_key> <apostrophe> <quotedbl> <Greek_iota>	: "ΐ"	U0390 # GREEK SMALL LETTER IOTA WITH DIALYTIKA AND TONOS
<dead_diaeresis> <Greek_IOTA>				: "Ϊ"	U03AA # GREEK CAPITAL LETTER IOTA WITH DIALYTIKA
<Multi_key> <quotedbl> <Greek_IOTA>			: "Ϊ"	U03AA # GREEK CAPITAL LETTER IOTA WITH DIALYTIKA
<Multi_key> <Greek_IOTA> <quotedbl>			: "Ϊ"	U03AA # GREEK CAPITAL LETTER IOTA WITH DIALYTIKA
<dead_diaeresis> <Greek_UPSILON>			: "Ϋ"	U03AB # GREEK CAPITAL LETTER UPSILON WITH DIALYTIKA
<Multi_key> <quotedbl> <Greek_UPSILON>			: "Ϋ"	U03AB # GREEK CAPITAL LETTER UPSILON WITH DIALYTIKA
<Multi_key> <Greek_UPSILON> <quotedbl>			: "Ϋ"	U03AB # GREEK CAPITAL LETTER UPSILON WITH DIALYTIKA
<dead_acute> <Greek_alpha>				: "ά"	U03AC # GREEK SMALL LETTER ALPHA WITH TONOS
<Multi_key> <acute> <Greek_alpha>			: "ά"	U03AC # GREEK SMALL LETTER ALPHA WITH TONOS
<Multi_key> <apostrophe> <Greek_alpha>			: "ά"	U03AC # GREEK SMALL LETTER ALPHA WITH TONOS
<Multi_key> <Greek_alpha> <apostrophe>			: "ά"	U03AC # GREEK SMALL LETTER ALPHA WITH TONOS
<dead_acute> <Greek_epsilon>				: "έ"	U03AD # GREEK SMALL LETTER EPSILON WITH TONOS
<Multi_key> <acute> <Greek_epsilon>			: "έ"	U03AD # GREEK SMALL LETTER EPSILON WITH TONOS
<Multi_key> <apostrophe> <Greek_epsilon>		: "έ"	U03AD # GREEK SMALL LETTER EPSILON WITH TONOS
<Multi_key> <Greek_epsilon> <apostrophe>		: "έ"	U03AD # GREEK SMALL LETTER EPSILON WITH TONOS
<dead_acute> <Greek_eta>				: "ή"	U03AE # GREEK SMALL LETTER ETA WITH TONOS
<Multi_key> <acute> <Greek_eta>				: "ή"	U03AE # GREEK SMALL LETTER ETA WITH TONOS
<Multi_key> <apostrophe> <Greek_eta>			: "ή"	U03AE # GREEK SMALL LETTER ETA WITH TONOS
<Multi_key> <Greek_eta> <apostrophe>			: "ή"	U03AE # GREEK SMALL LETTER ETA WITH TONOS
<dead_acute> <Greek_iota>				: "ί"	U03AF # GREEK SMALL LETTER IOTA WITH TONOS
<Multi_key> <acute> <Greek_iota>			: "ί"	U03AF # GREEK SMALL LETTER IOTA WITH TONOS
<Multi_key> <apostrophe> <Greek_iota>			: "ί"	U03AF # GREEK SMALL LETTER IOTA WITH TONOS
<dead_acute> <dead_diaeresis> <Greek_upsilon>		: "ΰ"	U03B0 # GREEK SMALL LETTER UPSILON WITH DIALYTIKA AND TONOS
<dead_acute> <Multi_key> <quotedbl> <Greek_upsilon>	: "ΰ"	U03B0 # GREEK SMALL LETTER UPSILON WITH DIALYTIKA AND TONOS
<Multi_key> <acute> <dead_diaeresis> <Greek_upsilon>	: "ΰ"	U03B0 # GREEK SMALL LETTER UPSILON WITH DIALYTIKA AND TONOS
<Multi_key> <acute> <quotedbl> <Greek_upsilon>		: "ΰ"	U03B0 # GREEK SMALL LETTER UPSILON WITH DIALYTIKA AND TONOS
<Multi_key> <apostrophe><dead_diaeresis> <Greek_upsilon>: "ΰ"	U03B0 # GREEK SMALL LETTER UPSILON WITH DIALYTIKA AND TONOS
<Multi_key> <apostrophe> <quotedbl> <Greek_upsilon>	: "ΰ"	U03B0 # GREEK SMALL LETTER UPSILON WITH DIALYTIKA AND TONOS
<dead_diaeresis> <dead_acute> <Greek_upsilon>		: "ΰ"	U03B0 # GREEK SMALL LETTER UPSILON WITH DIALYTIKA AND TONOS
<dead_diaeresis> <Greek_iota>				: "ϊ"	U03CA # GREEK SMALL LETTER IOTA WITH DIALYTIKA
<Multi_key> <quotedbl> <Greek_iota>			: "ϊ"	U03CA # GREEK SMALL LETTER IOTA WITH DIALYTIKA
<Multi_key> <Greek_iota> <quotedbl>			: "ϊ"	U03CA # GREEK SMALL LETTER IOTA WITH DIALYTIKA
<dead_diaeresis> <Greek_upsilon>			: "ϋ"	U03CB # GREEK SMALL LETTER UPSILON WITH DIALYTIKA
<Multi_key> <quotedbl> <Greek_upsilon>			: "ϋ"	U03CB # GREEK SMALL LETTER UPSILON WITH DIALYTIKA
<Multi_key> <Greek_upsilon> <quotedbl>			: "ϋ"	U03CB # GREEK SMALL LETTER UPSILON WITH DIALYTIKA
<dead_acute> <Greek_omicron>				: "ό"	U03CC # GREEK SMALL LETTER OMICRON WITH TONOS
<Multi_key> <acute> <Greek_omicron>			: "ό"	U03CC # GREEK SMALL LETTER OMICRON WITH TONOS
<Multi_key> <apostrophe> <Greek_omicron>		: "ό"	U03CC # GREEK SMALL LETTER OMICRON WITH TONOS
<Multi_key> <Greek_omicron> <apostrophe>		: "ό"	U03CC # GREEK SMALL LETTER OMICRON WITH TONOS
<dead_acute> <Greek_upsilon>				: "ύ"	U03CD # GREEK SMALL LETTER UPSILON WITH TONOS
<Multi_key> <acute> <Greek_upsilon>			: "ύ"	U03CD # GREEK SMALL LETTER UPSILON WITH TONOS
<Multi_key> <apostrophe> <Greek_upsilon>		: "ύ"	U03CD # GREEK SMALL LETTER UPSILON WITH TONOS
<Multi_key> <Greek_upsilon> <apostrophe>		: "ύ"	U03CD # GREEK SMALL LETTER UPSILON WITH TONOS
<dead_acute> <Greek_omega>				: "ώ"	U03CE # GREEK SMALL LETTER OMEGA WITH TONOS
<Multi_key> <acute> <Greek_omega>			: "ώ"	U03CE # GREEK SMALL LETTER OMEGA WITH TONOS
<Multi_key> <apostrophe> <Greek_omega>			: "ώ"	U03CE # GREEK SMALL LETTER OMEGA WITH TONOS
<Multi_key> <Greek_omega> <apostrophe>			: "ώ"	U03CE # GREEK SMALL LETTER OMEGA WITH TONOS
<Multi_key> <quotedbl> <U03D2>				: "ϔ"	U03D4 # GREEK UPSILON WITH DIAERESIS AND HOOK SYMBOL
# Cyrillic
<dead_grave> <Cyrillic_IE>		: "Ѐ"	U0400 # CYRILLIC CAPITAL LETTER IE WITH GRAVE
<Multi_key> <grave> <Cyrillic_IE>	: "Ѐ"	U0400 # CYRILLIC CAPITAL LETTER IE WITH GRAVE
<dead_diaeresis> <Cyrillic_IE>		: "Ё"	U0401 # CYRILLIC CAPITAL LETTER IO
<Multi_key> <quotedbl> <Cyrillic_IE>	: "Ё"	U0401 # CYRILLIC CAPITAL LETTER IO
<dead_acute> <Cyrillic_GHE>		: "Ѓ"	U0403 # CYRILLIC CAPITAL LETTER GJE
<Multi_key> <acute> <Cyrillic_GHE>	: "Ѓ"	U0403 # CYRILLIC CAPITAL LETTER GJE
<Multi_key> <apostrophe> <Cyrillic_GHE>	: "Ѓ"	U0403 # CYRILLIC CAPITAL LETTER GJE
<dead_diaeresis> <Ukrainian_I>		: "Ї"	U0407 # CYRILLIC CAPITAL LETTER YI
<Multi_key> <quotedbl> <Ukrainian_I>	: "Ї"	U0407 # CYRILLIC CAPITAL LETTER YI
<dead_acute> <Cyrillic_KA>		: "Ќ"	U040C # CYRILLIC CAPITAL LETTER KJE
<Multi_key> <acute> <Cyrillic_KA>	: "Ќ"	U040C # CYRILLIC CAPITAL LETTER KJE
<Multi_key> <apostrophe> <Cyrillic_KA>	: "Ќ"	U040C # CYRILLIC CAPITAL LETTER KJE
<dead_grave> <Cyrillic_I>		: "Ѝ"	U040D # CYRILLIC CAPITAL LETTER I WITH GRAVE
<Multi_key> <grave> <Cyrillic_I>	: "Ѝ"	U040D # CYRILLIC CAPITAL LETTER I WITH GRAVE
<dead_breve> <Cyrillic_U>		: "Ў"	U040E # CYRILLIC CAPITAL LETTER SHORT U
<Multi_key> <U> <Cyrillic_U>		: "Ў"	U040E # CYRILLIC CAPITAL LETTER SHORT U
<Multi_key> <b> <Cyrillic_U>		: "Ў"	U040E # CYRILLIC CAPITAL LETTER SHORT U
<dead_breve> <Cyrillic_I>		: "Й"	U0419 # CYRILLIC CAPITAL LETTER SHORT I
<Multi_key> <U> <Cyrillic_I>		: "Й"	U0419 # CYRILLIC CAPITAL LETTER SHORT I
<Multi_key> <b> <Cyrillic_I>		: "Й"	U0419 # CYRILLIC CAPITAL LETTER SHORT I
<dead_breve> <Cyrillic_i>		: "й"	U0439 # CYRILLIC SMALL LETTER SHORT I
<Multi_key> <U> <Cyrillic_i>		: "й"	U0439 # CYRILLIC SMALL LETTER SHORT I
<Multi_key> <b> <Cyrillic_i>		: "й"	U0439 # CYRILLIC SMALL LETTER SHORT I
<dead_grave> <Cyrillic_ie>		: "ѐ"	U0450 # CYRILLIC SMALL LETTER IE WITH GRAVE
<Multi_key> <grave> <Cyrillic_ie>	: "ѐ"	U0450 # CYRILLIC SMALL LETTER IE WITH GRAVE
<dead_diaeresis> <Cyrillic_ie>		: "ё"	U0451 # CYRILLIC SMALL LETTER IO
<Multi_key> <quotedbl> <Cyrillic_ie>	: "ё"	U0451 # CYRILLIC SMALL LETTER IO
<dead_acute> <Cyrillic_ghe>		: "ѓ"	U0453 # CYRILLIC SMALL LETTER GJE
<Multi_key> <acute> <Cyrillic_ghe>	: "ѓ"	U0453 # CYRILLIC SMALL LETTER GJE
<Multi_key> <apostrophe> <Cyrillic_ghe>	: "ѓ"	U0453 # CYRILLIC SMALL LETTER GJE
<dead_diaeresis> <Ukrainian_i>		: "ї"	U0457 # CYRILLIC SMALL LETTER YI
<Multi_key> <quotedbl> <Ukrainian_i>	: "ї"	U0457 # CYRILLIC SMALL LETTER YI
<dead_acute> <Cyrillic_ka>		: "ќ"	U045C # CYRILLIC SMALL LETTER KJE
<Multi_key> <acute> <Cyrillic_ka>	: "ќ"	U045C # CYRILLIC SMALL LETTER KJE
<Multi_key> <apostrophe> <Cyrillic_ka>	: "ќ"	U045C # CYRILLIC SMALL LETTER KJE
<dead_grave> <Cyrillic_i>		: "ѝ"	U045D # CYRILLIC SMALL LETTER I WITH GRAVE
<Multi_key> <grave> <Cyrillic_i>	: "ѝ"	U045D # CYRILLIC SMALL LETTER I WITH GRAVE
<dead_breve> <Cyrillic_u>		: "ў"	U045E # CYRILLIC SMALL LETTER SHORT U
<Multi_key> <U> <Cyrillic_u>		: "ў"	U045E # CYRILLIC SMALL LETTER SHORT U
<Multi_key> <b> <Cyrillic_u>		: "ў"	U045E # CYRILLIC SMALL LETTER SHORT U
<dead_doublegrave> <U0474>		: "Ѷ"	U0476 # CYRILLIC CAPITAL LETTER IZHITSA WITH DOUBLE GRAVE ACCENT
<dead_doublegrave> <U0475>		: "ѷ"	U0477 # CYRILLIC SMALL LETTER IZHITSA WITH DOUBLE GRAVE ACCENT
<Multi_key> <slash> <Cyrillic_GHE>	: "Ғ"	U0492 # CYRILLIC CAPITAL LETTER GHE WITH STROKE
<Multi_key> <KP_Divide> <Cyrillic_GHE>	: "Ғ"	U0492 # CYRILLIC CAPITAL LETTER GHE WITH STROKE
<Multi_key> <slash> <Cyrillic_ghe>	: "ғ"	U0493 # CYRILLIC SMALL LETTER GHE WITH STROKE
<Multi_key> <KP_Divide> <Cyrillic_ghe>	: "ғ"	U0493 # CYRILLIC SMALL LETTER GHE WITH STROKE
<Multi_key> <slash> <Cyrillic_KA>	: "Ҟ"	U049E # CYRILLIC CAPITAL LETTER KA WITH STROKE
<Multi_key> <KP_Divide> <Cyrillic_KA>	: "Ҟ"	U049E # CYRILLIC CAPITAL LETTER KA WITH STROKE
<Multi_key> <slash> <Cyrillic_ka>	: "ҟ"	U049F # CYRILLIC SMALL LETTER KA WITH STROKE
<Multi_key> <KP_Divide> <Cyrillic_ka>	: "ҟ"	U049F # CYRILLIC SMALL LETTER KA WITH STROKE
<Multi_key> <slash> <U04AE>		: "Ұ"	U04B0 # CYRILLIC CAPITAL LETTER STRAIGHT U WITH STROKE
<Multi_key> <KP_Divide> <U04AE>		: "Ұ"	U04B0 # CYRILLIC CAPITAL LETTER STRAIGHT U WITH STROKE
<Multi_key> <slash> <U04AF>		: "ұ"	U04B1 # CYRILLIC SMALL LETTER STRAIGHT U WITH STROKE
<Multi_key> <KP_Divide> <U04AF>		: "ұ"	U04B1 # CYRILLIC SMALL LETTER STRAIGHT U WITH STROKE
<dead_breve> <Cyrillic_ZHE>		: "Ӂ"	U04C1 # CYRILLIC CAPITAL LETTER ZHE WITH BREVE
<Multi_key> <U> <Cyrillic_ZHE>		: "Ӂ"	U04C1 # CYRILLIC CAPITAL LETTER ZHE WITH BREVE
<Multi_key> <b> <Cyrillic_ZHE>		: "Ӂ"	U04C1 # CYRILLIC CAPITAL LETTER ZHE WITH BREVE
<dead_breve> <Cyrillic_zhe>		: "ӂ"	U04C2 # CYRILLIC SMALL LETTER ZHE WITH BREVE
<Multi_key> <U> <Cyrillic_zhe>		: "ӂ"	U04C2 # CYRILLIC SMALL LETTER ZHE WITH BREVE
<Multi_key> <b> <Cyrillic_zhe>		: "ӂ"	U04C2 # CYRILLIC SMALL LETTER ZHE WITH BREVE
<dead_breve> <Cyrillic_A>		: "Ӑ"	U04D0 # CYRILLIC CAPITAL LETTER A WITH BREVE
<Multi_key> <U> <Cyrillic_A>		: "Ӑ"	U04D0 # CYRILLIC CAPITAL LETTER A WITH BREVE
<Multi_key> <b> <Cyrillic_A>		: "Ӑ"	U04D0 # CYRILLIC CAPITAL LETTER A WITH BREVE
<dead_breve> <Cyrillic_a>		: "ӑ"	U04D1 # CYRILLIC SMALL LETTER A WITH BREVE
<Multi_key> <U> <Cyrillic_a>		: "ӑ"	U04D1 # CYRILLIC SMALL LETTER A WITH BREVE
<Multi_key> <b> <Cyrillic_a>		: "ӑ"	U04D1 # CYRILLIC SMALL LETTER A WITH BREVE
<dead_diaeresis> <Cyrillic_A>		: "Ӓ"	U04D2 # CYRILLIC CAPITAL LETTER A WITH DIAERESIS
<Multi_key> <quotedbl> <Cyrillic_A>	: "Ӓ"	U04D2 # CYRILLIC CAPITAL LETTER A WITH DIAERESIS
<dead_diaeresis> <Cyrillic_a>		: "ӓ"	U04D3 # CYRILLIC SMALL LETTER A WITH DIAERESIS
<Multi_key> <quotedbl> <Cyrillic_a>	: "ӓ"	U04D3 # CYRILLIC SMALL LETTER A WITH DIAERESIS
<dead_breve> <Cyrillic_IE>		: "Ӗ"	U04D6 # CYRILLIC CAPITAL LETTER IE WITH BREVE
<Multi_key> <U> <Cyrillic_IE>		: "Ӗ"	U04D6 # CYRILLIC CAPITAL LETTER IE WITH BREVE
<Multi_key> <b> <Cyrillic_IE>		: "Ӗ"	U04D6 # CYRILLIC CAPITAL LETTER IE WITH BREVE
<dead_breve> <Cyrillic_ie>		: "ӗ"	U04D7 # CYRILLIC SMALL LETTER IE WITH BREVE
<Multi_key> <U> <Cyrillic_ie>		: "ӗ"	U04D7 # CYRILLIC SMALL LETTER IE WITH BREVE
<Multi_key> <b> <Cyrillic_ie>		: "ӗ"	U04D7 # CYRILLIC SMALL LETTER IE WITH BREVE
<dead_diaeresis> <U04D8>		: "Ӛ"	U04DA # CYRILLIC CAPITAL LETTER SCHWA WITH DIAERESIS
<Multi_key> <quotedbl> <U04D8>		: "Ӛ"	U04DA # CYRILLIC CAPITAL LETTER SCHWA WITH DIAERESIS
<dead_diaeresis> <U04D9>		: "ӛ"	U04DB # CYRILLIC SMALL LETTER SCHWA WITH DIAERESIS
<Multi_key> <quotedbl> <U04D9>		: "ӛ"	U04DB # CYRILLIC SMALL LETTER SCHWA WITH DIAERESIS
<dead_diaeresis> <Cyrillic_ZHE>		: "Ӝ"	U04DC # CYRILLIC CAPITAL LETTER ZHE WITH DIAERESIS
<Multi_key> <quotedbl> <Cyrillic_ZHE>	: "Ӝ"	U04DC # CYRILLIC CAPITAL LETTER ZHE WITH DIAERESIS
<dead_diaeresis> <Cyrillic_zhe>		: "ӝ"	U04DD # CYRILLIC SMALL LETTER ZHE WITH DIAERESIS
<Multi_key> <quotedbl> <Cyrillic_zhe>	: "ӝ"	U04DD # CYRILLIC SMALL LETTER ZHE WITH DIAERESIS
<dead_diaeresis> <Cyrillic_ZE>		: "Ӟ"	U04DE # CYRILLIC CAPITAL LETTER ZE WITH DIAERESIS
<Multi_key> <quotedbl> <Cyrillic_ZE>	: "Ӟ"	U04DE # CYRILLIC CAPITAL LETTER ZE WITH DIAERESIS
<dead_diaeresis> <Cyrillic_ze>		: "ӟ"	U04DF # CYRILLIC SMALL LETTER ZE WITH DIAERESIS
<Multi_key> <quotedbl> <Cyrillic_ze>	: "ӟ"	U04DF # CYRILLIC SMALL LETTER ZE WITH DIAERESIS
<dead_macron> <Cyrillic_I>		: "Ӣ"	U04E2 # CYRILLIC CAPITAL LETTER I WITH MACRON
<Multi_key> <macron> <Cyrillic_I>	: "Ӣ"	U04E2 # CYRILLIC CAPITAL LETTER I WITH MACRON
<Multi_key> <underscore> <Cyrillic_I>	: "Ӣ"	U04E2 # CYRILLIC CAPITAL LETTER I WITH MACRON
<dead_macron> <Cyrillic_i>		: "ӣ"	U04E3 # CYRILLIC SMALL LETTER I WITH MACRON
<Multi_key> <macron> <Cyrillic_i>	: "ӣ"	U04E3 # CYRILLIC SMALL LETTER I WITH MACRON
<Multi_key> <underscore> <Cyrillic_i>	: "ӣ"	U04E3 # CYRILLIC SMALL LETTER I WITH MACRON
<dead_diaeresis> <Cyrillic_I>		: "Ӥ"	U04E4 # CYRILLIC CAPITAL LETTER I WITH DIAERESIS
<Multi_key> <quotedbl> <Cyrillic_I>	: "Ӥ"	U04E4 # CYRILLIC CAPITAL LETTER I WITH DIAERESIS
<dead_diaeresis> <Cyrillic_i>		: "ӥ"	U04E5 # CYRILLIC SMALL LETTER I WITH DIAERESIS
<Multi_key> <quotedbl> <Cyrillic_i>	: "ӥ"	U04E5 # CYRILLIC SMALL LETTER I WITH DIAERESIS
<dead_diaeresis> <Cyrillic_O>		: "Ӧ"	U04E6 # CYRILLIC CAPITAL LETTER O WITH DIAERESIS
<Multi_key> <quotedbl> <Cyrillic_O>	: "Ӧ"	U04E6 # CYRILLIC CAPITAL LETTER O WITH DIAERESIS
<dead_diaeresis> <Cyrillic_o>		: "ӧ"	U04E7 # CYRILLIC SMALL LETTER O WITH DIAERESIS
<Multi_key> <quotedbl> <Cyrillic_o>	: "ӧ"	U04E7 # CYRILLIC SMALL LETTER O WITH DIAERESIS
<dead_diaeresis> <U04E8>		: "Ӫ"	U04EA # CYRILLIC CAPITAL LETTER BARRED O WITH DIAERESIS
<Multi_key> <quotedbl> <U04E8>		: "Ӫ"	U04EA # CYRILLIC CAPITAL LETTER BARRED O WITH DIAERESIS
<dead_diaeresis> <U04E9>		: "ӫ"	U04EB # CYRILLIC SMALL LETTER BARRED O WITH DIAERESIS
<Multi_key> <quotedbl> <U04E9>		: "ӫ"	U04EB # CYRILLIC SMALL LETTER BARRED O WITH DIAERESIS
<dead_diaeresis> <Cyrillic_E>		: "Ӭ"	U04EC # CYRILLIC CAPITAL LETTER E WITH DIAERESIS
<Multi_key> <quotedbl> <Cyrillic_E>	: "Ӭ"	U04EC # CYRILLIC CAPITAL LETTER E WITH DIAERESIS
<dead_diaeresis> <Cyrillic_e>		: "ӭ"	U04ED # CYRILLIC SMALL LETTER E WITH DIAERESIS
<Multi_key> <quotedbl> <Cyrillic_e>	: "ӭ"	U04ED # CYRILLIC SMALL LETTER E WITH DIAERESIS
<dead_macron> <Cyrillic_U>		: "Ӯ"	U04EE # CYRILLIC CAPITAL LETTER U WITH MACRON
<Multi_key> <macron> <Cyrillic_U>	: "Ӯ"	U04EE # CYRILLIC CAPITAL LETTER U WITH MACRON
<Multi_key> <underscore> <Cyrillic_U>	: "Ӯ"	U04EE # CYRILLIC CAPITAL LETTER U WITH MACRON
<dead_macron> <Cyrillic_u>		: "ӯ"	U04EF # CYRILLIC SMALL LETTER U WITH MACRON
<Multi_key> <macron> <Cyrillic_u>	: "ӯ"	U04EF # CYRILLIC SMALL LETTER U WITH MACRON
<Multi_key> <underscore> <Cyrillic_u>	: "ӯ"	U04EF # CYRILLIC SMALL LETTER U WITH MACRON
<dead_diaeresis> <Cyrillic_U>		: "Ӱ"	U04F0 # CYRILLIC CAPITAL LETTER U WITH DIAERESIS
<Multi_key> <quotedbl> <Cyrillic_U>	: "Ӱ"	U04F0 # CYRILLIC CAPITAL LETTER U WITH DIAERESIS
<dead_diaeresis> <Cyrillic_u>		: "ӱ"	U04F1 # CYRILLIC SMALL LETTER U WITH DIAERESIS
<Multi_key> <quotedbl> <Cyrillic_u>	: "ӱ"	U04F1 # CYRILLIC SMALL LETTER U WITH DIAERESIS
<dead_doubleacute> <Cyrillic_U>		: "Ӳ"	U04F2 # CYRILLIC CAPITAL LETTER U WITH DOUBLE ACUTE
<Multi_key> <equal> <Cyrillic_U>	: "Ӳ"	U04F2 # CYRILLIC CAPITAL LETTER U WITH DOUBLE ACUTE
<dead_doubleacute> <Cyrillic_u>		: "ӳ"	U04F3 # CYRILLIC SMALL LETTER U WITH DOUBLE ACUTE
<Multi_key> <equal> <Cyrillic_u>	: "ӳ"	U04F3 # CYRILLIC SMALL LETTER U WITH DOUBLE ACUTE
<dead_diaeresis> <Cyrillic_CHE>		: "Ӵ"	U04F4 # CYRILLIC CAPITAL LETTER CHE WITH DIAERESIS
<Multi_key> <quotedbl> <Cyrillic_CHE>	: "Ӵ"	U04F4 # CYRILLIC CAPITAL LETTER CHE WITH DIAERESIS
<dead_diaeresis> <Cyrillic_che>		: "ӵ"	U04F5 # CYRILLIC SMALL LETTER CHE WITH DIAERESIS
<Multi_key> <quotedbl> <Cyrillic_che>	: "ӵ"	U04F5 # CYRILLIC SMALL LETTER CHE WITH DIAERESIS
<dead_diaeresis> <Cyrillic_YERU>	: "Ӹ"	U04F8 # CYRILLIC CAPITAL LETTER YERU WITH DIAERESIS
<Multi_key> <quotedbl> <Cyrillic_YERU>	: "Ӹ"	U04F8 # CYRILLIC CAPITAL LETTER YERU WITH DIAERESIS
<dead_diaeresis> <Cyrillic_yeru>	: "ӹ"	U04F9 # CYRILLIC SMALL LETTER YERU WITH DIAERESIS
<Multi_key> <quotedbl> <Cyrillic_yeru>	: "ӹ"	U04F9 # CYRILLIC SMALL LETTER YERU WITH DIAERESIS
# Several other scripts
<Multi_key> <U0653> <Arabic_alef>	: "آ"	U0622 # ARABIC LETTER ALEF WITH MADDA ABOVE
<Multi_key> <U0654> <Arabic_alef>	: "أ"	U0623 # ARABIC LETTER ALEF WITH HAMZA ABOVE
<Multi_key> <U0654> <Arabic_waw>	: "ؤ"	U0624 # ARABIC LETTER WAW WITH HAMZA ABOVE
<Multi_key> <U0655> <Arabic_alef>	: "إ"	U0625 # ARABIC LETTER ALEF WITH HAMZA BELOW
<Multi_key> <U0654> <Arabic_yeh>	: "ئ"	U0626 # ARABIC LETTER YEH WITH HAMZA ABOVE
<Multi_key> <U0654> <U06D5>		: "ۀ"	U06C0 # ARABIC LETTER HEH WITH YEH ABOVE
<Multi_key> <U0654> <U06C1>		: "ۂ"	U06C2 # ARABIC LETTER HEH GOAL WITH HAMZA ABOVE
<Multi_key> <U0654> <U06D2>		: "ۓ"	U06D3 # ARABIC LETTER YEH BARREE WITH HAMZA ABOVE
<Multi_key> <U093C> <U0928>		: "ऩ"	U0929 # DEVANAGARI LETTER NNNA
<Multi_key> <U093C> <U0930>		: "ऱ"	U0931 # DEVANAGARI LETTER RRA
<Multi_key> <U093C> <U0933>		: "ऴ"	U0934 # DEVANAGARI LETTER LLLA
<Multi_key> <U093C> <U0915>		: "क़"	U0958 # DEVANAGARI LETTER QA
<Multi_key> <U093C> <U0916>		: "ख़"	U0959 # DEVANAGARI LETTER KHHA
<Multi_key> <U093C> <U0917>		: "ग़"	U095A # DEVANAGARI LETTER GHHA
<Multi_key> <U093C> <U091C>		: "ज़"	U095B # DEVANAGARI LETTER ZA
<Multi_key> <U093C> <U0921>		: "ड़"	U095C # DEVANAGARI LETTER DDDHA
<Multi_key> <U093C> <U0922>		: "ढ़"	U095D # DEVANAGARI LETTER RHA
<Multi_key> <U093C> <U092B>		: "फ़"	U095E # DEVANAGARI LETTER FA
<Multi_key> <U093C> <U092F>		: "य़"	U095F # DEVANAGARI LETTER YYA
<Multi_key> <U09C7> <U09BE>		: "ো"	U09CB # BENGALI VOWEL SIGN O
<Multi_key> <U09C7> <U09D7>		: "ৌ"	U09CC # BENGALI VOWEL SIGN AU
<Multi_key> <U09BC> <U09A1>		: "ড়"	U09DC # BENGALI LETTER RRA
<Multi_key> <U09BC> <U09A2>		: "ঢ়"	U09DD # BENGALI LETTER RHA
<Multi_key> <U09BC> <U09AF>		: "য়"	U09DF # BENGALI LETTER YYA
<Multi_key> <U0A3C> <U0A32>		: "ਲ਼"	U0A33 # GURMUKHI LETTER LLA
<Multi_key> <U0A3C> <U0A38>		: "ਸ਼"	U0A36 # GURMUKHI LETTER SHA
<Multi_key> <U0A3C> <U0A16>		: "ਖ਼"	U0A59 # GURMUKHI LETTER KHHA
<Multi_key> <U0A3C> <U0A17>		: "ਗ਼"	U0A5A # GURMUKHI LETTER GHHA
<Multi_key> <U0A3C> <U0A1C>		: "ਜ਼"	U0A5B # GURMUKHI LETTER ZA
<Multi_key> <U0A3C> <U0A2B>		: "ਫ਼"	U0A5E # GURMUKHI LETTER FA
<Multi_key> <U0B47> <U0B56>		: "ୈ"	U0B48 # ORIYA VOWEL SIGN AI
<Multi_key> <U0B47> <U0B3E>		: "ୋ"	U0B4B # ORIYA VOWEL SIGN O
<Multi_key> <U0B47> <U0B57>		: "ୌ"	U0B4C # ORIYA VOWEL SIGN AU
<Multi_key> <U0B3C> <U0B21>		: "ଡ଼"	U0B5C # ORIYA LETTER RRA
<Multi_key> <U0B3C> <U0B22>		: "ଢ଼"	U0B5D # ORIYA LETTER RHA
<Multi_key> <U0BD7> <U0B92>		: "ஔ"	U0B94 # TAMIL LETTER AU
<Multi_key> <U0BC6> <U0BBE>		: "ொ"	U0BCA # TAMIL VOWEL SIGN O
<Multi_key> <U0BC7> <U0BBE>		: "ோ"	U0BCB # TAMIL VOWEL SIGN OO
<Multi_key> <U0BC6> <U0BD7>		: "ௌ"	U0BCC # TAMIL VOWEL SIGN AU
<Multi_key> <U0C46> <U0C56>		: "ై"	U0C48 # TELUGU VOWEL SIGN AI
<Multi_key> <U0CBF> <U0CD5>		: "ೀ"	U0CC0 # KANNADA VOWEL SIGN II
<Multi_key> <U0CC6> <U0CD5>		: "ೇ"	U0CC7 # KANNADA VOWEL SIGN EE
<Multi_key> <U0CC6> <U0CD6>		: "ೈ"	U0CC8 # KANNADA VOWEL SIGN AI
<Multi_key> <U0CC6> <U0CC2>		: "ೊ"	U0CCA # KANNADA VOWEL SIGN O
<Multi_key> <U0CCA> <U0CD5>		: "ೋ"	U0CCB # KANNADA VOWEL SIGN OO
<Multi_key> <U0D46> <U0D3E>		: "ൊ"	U0D4A # MALAYALAM VOWEL SIGN O
<Multi_key> <U0D47> <U0D3E>		: "ോ"	U0D4B # MALAYALAM VOWEL SIGN OO
<Multi_key> <U0D46> <U0D57>		: "ൌ"	U0D4C # MALAYALAM VOWEL SIGN AU
<Multi_key> <U0DD9> <U0DCA>		: "ේ"	U0DDA # SINHALA VOWEL SIGN DIGA KOMBUVA
<Multi_key> <U0DD9> <U0DCF>		: "ො"	U0DDC # SINHALA VOWEL SIGN KOMBUVA HAA AELA-PILLA
<Multi_key> <U0DDC> <U0DCA>		: "ෝ"	U0DDD # SINHALA VOWEL SIGN KOMBUVA HAA DIGA AELA-PILLA
<Multi_key> <U0DD9> <U0DDF>		: "ෞ"	U0DDE # SINHALA VOWEL SIGN KOMBUVA HAA GAYANUKITTA
<Multi_key> <U0FB7> <U0F42>		: "གྷ"	U0F43 # TIBETAN LETTER GHA
<Multi_key> <U0FB7> <U0F4C>		: "ཌྷ"	U0F4D # TIBETAN LETTER DDHA
<Multi_key> <U0FB7> <U0F51>		: "དྷ"	U0F52 # TIBETAN LETTER DHA
<Multi_key> <U0FB7> <U0F56>		: "བྷ"	U0F57 # TIBETAN LETTER BHA
<Multi_key> <U0FB7> <U0F5B>		: "ཛྷ"	U0F5C # TIBETAN LETTER DZHA
<Multi_key> <U0FB5> <U0F40>		: "ཀྵ"	U0F69 # TIBETAN LETTER KSSA
<Multi_key> <U0F71> <U0F72>		: "ཱི"	U0F73 # TIBETAN VOWEL SIGN II
<Multi_key> <U0F71> <U0F74>		: "ཱུ"	U0F75 # TIBETAN VOWEL SIGN UU
<Multi_key> <U0FB2> <U0F80>		: "ྲྀ"	U0F76 # TIBETAN VOWEL SIGN VOCALIC R
<Multi_key> <U0FB3> <U0F80>		: "ླྀ"	U0F78 # TIBETAN VOWEL SIGN VOCALIC L
<Multi_key> <U0F71> <U0F80>		: "ཱྀ"	U0F81 # TIBETAN VOWEL SIGN REVERSED II
<Multi_key> <U0F92> <U0FB7>		: "ྒྷ"	U0F93 # TIBETAN SUBJOINED LETTER GHA
<Multi_key> <U0F9C> <U0FB7>		: "ྜྷ"	U0F9D # TIBETAN SUBJOINED LETTER DDHA
<Multi_key> <U0FA1> <U0FB7>		: "ྡྷ"	U0FA2 # TIBETAN SUBJOINED LETTER DHA
<Multi_key> <U0FA6> <U0FB7>		: "ྦྷ"	U0FA7 # TIBETAN SUBJOINED LETTER BHA
<Multi_key> <U0FAB> <U0FB7>		: "ྫྷ"	U0FAC # TIBETAN SUBJOINED LETTER DZHA
<Multi_key> <U0F90> <U0FB5>		: "ྐྵ"	U0FB9 # TIBETAN SUBJOINED LETTER KSSA
<Multi_key> <U102E> <U1025>		: "ဦ"	U1026 # MYANMAR LETTER UU
# Conjoining Jamo for Korean Hangul
<Multi_key> <U1100> <U1100>		: "ᄁ"	U1101 # HANGUL CHOSEONG SSANGKIYEOK
<Multi_key> <U1103> <U1103>		: "ᄄ"	U1104 # HANGUL CHOSEONG SSANGTIKEUT
<Multi_key> <U1107> <U1107>		: "ᄈ"	U1108 # HANGUL CHOSEONG SSANGPIEUP
<Multi_key> <U1109> <U1109>		: "ᄊ"	U110a # HANGUL CHOSEONG SSANGSIOS
<Multi_key> <U110C> <U110C>		: "ᄍ"	U110d # HANGUL CHOSEONG SSANGCIEUC
<Multi_key> <U1102> <U1100>		: "ᄓ"	U1113 # HANGUL CHOSEONG NIEUN-KIYEOK
<Multi_key> <U1102> <U1102>		: "ᄔ"	U1114 # HANGUL CHOSEONG SSANGNIEUN
<Multi_key> <U1102> <U1103>		: "ᄕ"	U1115 # HANGUL CHOSEONG NIEUN-TIKEUT
<Multi_key> <U1102> <U1107>		: "ᄖ"	U1116 # HANGUL CHOSEONG NIEUN-PIEUP
<Multi_key> <U1103> <U1100>		: "ᄗ"	U1117 # HANGUL CHOSEONG TIKEUT-KIYEOK
<Multi_key> <U1105> <U1102>		: "ᄘ"	U1118 # HANGUL CHOSEONG RIEUL-NIEUN
<Multi_key> <U1105> <U1105>		: "ᄙ"	U1119 # HANGUL CHOSEONG SSANGRIEUL
<Multi_key> <U1105> <U1112>		: "ᄚ"	U111a # HANGUL CHOSEONG RIEUL-HIEUH
<Multi_key> <U1105> <U110B>		: "ᄛ"	U111b # HANGUL CHOSEONG KAPYEOUNRIEUL
<Multi_key> <U1106> <U1107>		: "ᄜ"	U111c # HANGUL CHOSEONG MIEUM-PIEUP
<Multi_key> <U1106> <U110B>		: "ᄝ"	U111d # HANGUL CHOSEONG KAPYEOUNMIEUM
<Multi_key> <U1107> <U1100>		: "ᄞ"	U111e # HANGUL CHOSEONG PIEUP-KIYEOK
<Multi_key> <U1107> <U1102>		: "ᄟ"	U111f # HANGUL CHOSEONG PIEUP-NIEUN
<Multi_key> <U1107> <U1103>		: "ᄠ"	U1120 # HANGUL CHOSEONG PIEUP-TIKEUT
<Multi_key> <U1107> <U1109>		: "ᄡ"	U1121 # HANGUL CHOSEONG PIEUP-SIOS
<Multi_key> <U1107> <U110C>		: "ᄧ"	U1127 # HANGUL CHOSEONG PIEUP-CIEUC
<Multi_key> <U1107> <U110E>		: "ᄨ"	U1128 # HANGUL CHOSEONG PIEUP-CHIEUCH
<Multi_key> <U1107> <U1110>		: "ᄩ"	U1129 # HANGUL CHOSEONG PIEUP-THIEUTH
<Multi_key> <U1107> <U1111>		: "ᄪ"	U112a # HANGUL CHOSEONG PIEUP-PHIEUPH
<Multi_key> <U1107> <U110B>		: "ᄫ"	U112b # HANGUL CHOSEONG KAPYEOUNPIEUP
<Multi_key> <U1109> <U1100>		: "ᄭ"	U112d # HANGUL CHOSEONG SIOS-KIYEOK
<Multi_key> <U1109> <U1102>		: "ᄮ"	U112e # HANGUL CHOSEONG SIOS-NIEUN
<Multi_key> <U1109> <U1103>		: "ᄯ"	U112f # HANGUL CHOSEONG SIOS-TIKEUT
<Multi_key> <U1109> <U1105>		: "ᄰ"	U1130 # HANGUL CHOSEONG SIOS-RIEUL
<Multi_key> <U1109> <U1106>		: "ᄱ"	U1131 # HANGUL CHOSEONG SIOS-MIEUM
<Multi_key> <U1109> <U1107>		: "ᄲ"	U1132 # HANGUL CHOSEONG SIOS-PIEUP
<Multi_key> <U1109> <U110B>		: "ᄵ"	U1135 # HANGUL CHOSEONG SIOS-IEUNG
<Multi_key> <U1109> <U110C>		: "ᄶ"	U1136 # HANGUL CHOSEONG SIOS-CIEUC
<Multi_key> <U1109> <U110E>		: "ᄷ"	U1137 # HANGUL CHOSEONG SIOS-CHIEUCH
<Multi_key> <U1109> <U110F>		: "ᄸ"	U1138 # HANGUL CHOSEONG SIOS-KHIEUKH
<Multi_key> <U1109> <U1110>		: "ᄹ"	U1139 # HANGUL CHOSEONG SIOS-THIEUTH
<Multi_key> <U1109> <U1111>		: "ᄺ"	U113a # HANGUL CHOSEONG SIOS-PHIEUPH
<Multi_key> <U1109> <U1112>		: "ᄻ"	U113b # HANGUL CHOSEONG SIOS-HIEUH
<Multi_key> <U113C> <U113C>		: "ᄽ"	U113d # HANGUL CHOSEONG CHITUEUMSSANGSIOS
<Multi_key> <U113E> <U113E>		: "ᄿ"	U113f # HANGUL CHOSEONG CEONGCHIEUMSSANGSIOS
<Multi_key> <U110B> <U1100>		: "ᅁ"	U1141 # HANGUL CHOSEONG IEUNG-KIYEOK
<Multi_key> <U110B> <U1103>		: "ᅂ"	U1142 # HANGUL CHOSEONG IEUNG-TIKEUT
<Multi_key> <U110B> <U1106>		: "ᅃ"	U1143 # HANGUL CHOSEONG IEUNG-MIEUM
<Multi_key> <U110B> <U1107>		: "ᅄ"	U1144 # HANGUL CHOSEONG IEUNG-PIEUP
<Multi_key> <U110B> <U1109>		: "ᅅ"	U1145 # HANGUL CHOSEONG IEUNG-SIOS
<Multi_key> <U110B> <U1140>		: "ᅆ"	U1146 # HANGUL CHOSEONG IEUNG-PANSIOS
<Multi_key> <U110B> <U110B>		: "ᅇ"	U1147 # HANGUL CHOSEONG SSANGIEUNG
<Multi_key> <U110B> <U110C>		: "ᅈ"	U1148 # HANGUL CHOSEONG IEUNG-CIEUC
<Multi_key> <U110B> <U110E>		: "ᅉ"	U1149 # HANGUL CHOSEONG IEUNG-CHIEUCH
<Multi_key> <U110B> <U1110>		: "ᅊ"	U114a # HANGUL CHOSEONG IEUNG-THIEUTH
<Multi_key> <U110B> <U1111>		: "ᅋ"	U114b # HANGUL CHOSEONG IEUNG-PHIEUPH
<Multi_key> <U110C> <U110B>		: "ᅍ"	U114d # HANGUL CHOSEONG CIEUC-IEUNG
<Multi_key> <U114E> <U114E>		: "ᅏ"	U114f # HANGUL CHOSEONG CHITUEUMSSANGCIEUC
<Multi_key> <U1150> <U1150>		: "ᅑ"	U1151 # HANGUL CHOSEONG CEONGCHIEUMSSANGCIEUC
<Multi_key> <U110E> <U110F>		: "ᅒ"	U1152 # HANGUL CHOSEONG CHIEUCH-KHIEUKH
<Multi_key> <U110E> <U1112>		: "ᅓ"	U1153 # HANGUL CHOSEONG CHIEUCH-HIEUH
<Multi_key> <U1111> <U1107>		: "ᅖ"	U1156 # HANGUL CHOSEONG PHIEUPH-PIEUP
<Multi_key> <U1111> <U110B>		: "ᅗ"	U1157 # HANGUL CHOSEONG KAPYEOUNPHIEUPH
<Multi_key> <U1112> <U1112>		: "ᅘ"	U1158 # HANGUL CHOSEONG SSANGHIEUH
<Multi_key> <U1161> <U1175>		: "ᅢ"	U1162 # HANGUL JUNGSEONG AE
<Multi_key> <U1163> <U1175>		: "ᅤ"	U1164 # HANGUL JUNGSEONG YAE
<Multi_key> <U1165> <U1175>		: "ᅦ"	U1166 # HANGUL JUNGSEONG E
<Multi_key> <U1167> <U1175>		: "ᅨ"	U1168 # HANGUL JUNGSEONG YE
<Multi_key> <U1169> <U1161>		: "ᅪ"	U116a # HANGUL JUNGSEONG WA
<Multi_key> <U1169> <U1175>		: "ᅬ"	U116c # HANGUL JUNGSEONG OE
<Multi_key> <U116E> <U1165>		: "ᅯ"	U116f # HANGUL JUNGSEONG WEO
<Multi_key> <U116E> <U1175>		: "ᅱ"	U1171 # HANGUL JUNGSEONG WI
<Multi_key> <U1173> <U1175>		: "ᅴ"	U1174 # HANGUL JUNGSEONG YI
<Multi_key> <U1161> <U1169>		: "ᅶ"	U1176 # HANGUL JUNGSEONG A-O
<Multi_key> <U1161> <U116E>		: "ᅷ"	U1177 # HANGUL JUNGSEONG A-U
<Multi_key> <U1163> <U1169>		: "ᅸ"	U1178 # HANGUL JUNGSEONG YA-O
<Multi_key> <U1163> <U116D>		: "ᅹ"	U1179 # HANGUL JUNGSEONG YA-YO
<Multi_key> <U1165> <U1169>		: "ᅺ"	U117a # HANGUL JUNGSEONG EO-O
<Multi_key> <U1165> <U116E>		: "ᅻ"	U117b # HANGUL JUNGSEONG EO-U
<Multi_key> <U1165> <U1173>		: "ᅼ"	U117c # HANGUL JUNGSEONG EO-EU
<Multi_key> <U1167> <U1169>		: "ᅽ"	U117d # HANGUL JUNGSEONG YEO-O
<Multi_key> <U1167> <U116E>		: "ᅾ"	U117e # HANGUL JUNGSEONG YEO-U
<Multi_key> <U1169> <U1165>		: "ᅿ"	U117f # HANGUL JUNGSEONG O-EO
<Multi_key> <U1169> <U1166>		: "ᆀ"	U1180 # HANGUL JUNGSEONG O-E
<Multi_key> <U1169> <U1168>		: "ᆁ"	U1181 # HANGUL JUNGSEONG O-YE
<Multi_key> <U1169> <U1169>		: "ᆂ"	U1182 # HANGUL JUNGSEONG O-O
<Multi_key> <U1169> <U116E>		: "ᆃ"	U1183 # HANGUL JUNGSEONG O-U
<Multi_key> <U116D> <U1163>		: "ᆄ"	U1184 # HANGUL JUNGSEONG YO-YA
<Multi_key> <U116D> <U1164>		: "ᆅ"	U1185 # HANGUL JUNGSEONG YO-YAE
<Multi_key> <U116D> <U1167>		: "ᆆ"	U1186 # HANGUL JUNGSEONG YO-YEO
<Multi_key> <U116D> <U1169>		: "ᆇ"	U1187 # HANGUL JUNGSEONG YO-O
<Multi_key> <U116D> <U1175>		: "ᆈ"	U1188 # HANGUL JUNGSEONG YO-I
<Multi_key> <U116E> <U1161>		: "ᆉ"	U1189 # HANGUL JUNGSEONG U-A
<Multi_key> <U116E> <U1162>		: "ᆊ"	U118a # HANGUL JUNGSEONG U-AE
<Multi_key> <U116E> <U1168>		: "ᆌ"	U118c # HANGUL JUNGSEONG U-YE
<Multi_key> <U116E> <U116E>		: "ᆍ"	U118d # HANGUL JUNGSEONG U-U
<Multi_key> <U1172> <U1161>		: "ᆎ"	U118e # HANGUL JUNGSEONG YU-A
<Multi_key> <U1172> <U1165>		: "ᆏ"	U118f # HANGUL JUNGSEONG YU-EO
<Multi_key> <U1172> <U1166>		: "ᆐ"	U1190 # HANGUL JUNGSEONG YU-E
<Multi_key> <U1172> <U1167>		: "ᆑ"	U1191 # HANGUL JUNGSEONG YU-YEO
<Multi_key> <U1172> <U1168>		: "ᆒ"	U1192 # HANGUL JUNGSEONG YU-YE
<Multi_key> <U1172> <U116E>		: "ᆓ"	U1193 # HANGUL JUNGSEONG YU-U
<Multi_key> <U1172> <U1175>		: "ᆔ"	U1194 # HANGUL JUNGSEONG YU-I
<Multi_key> <U1173> <U116E>		: "ᆕ"	U1195 # HANGUL JUNGSEONG EU-U
<Multi_key> <U1173> <U1173>		: "ᆖ"	U1196 # HANGUL JUNGSEONG EU-EU
<Multi_key> <U1174> <U116E>		: "ᆗ"	U1197 # HANGUL JUNGSEONG YI-U
<Multi_key> <U1175> <U1161>		: "ᆘ"	U1198 # HANGUL JUNGSEONG I-A
<Multi_key> <U1175> <U1163>		: "ᆙ"	U1199 # HANGUL JUNGSEONG I-YA
<Multi_key> <U1175> <U1169>		: "ᆚ"	U119a # HANGUL JUNGSEONG I-O
<Multi_key> <U1175> <U116E>		: "ᆛ"	U119b # HANGUL JUNGSEONG I-U
<Multi_key> <U1175> <U1173>		: "ᆜ"	U119c # HANGUL JUNGSEONG I-EU
<Multi_key> <U1175> <U119E>		: "ᆝ"	U119d # HANGUL JUNGSEONG I-ARAEA
<Multi_key> <U119E> <U1165>		: "ᆟ"	U119f # HANGUL JUNGSEONG ARAEA-EO
<Multi_key> <U119E> <U116E>		: "ᆠ"	U11a0 # HANGUL JUNGSEONG ARAEA-U
<Multi_key> <U119E> <U1175>		: "ᆡ"	U11a1 # HANGUL JUNGSEONG ARAEA-I
<Multi_key> <U119E> <U119E>		: "ᆢ"	U11a2 # HANGUL JUNGSEONG SSANGARAEA
<Multi_key> <U11A8> <U11A8>		: "ᆩ"	U11a9 # HANGUL JONGSEONG SSANGKIYEOK
<Multi_key> <U11A8> <U11BA>		: "ᆪ"	U11aa # HANGUL JONGSEONG KIYEOK-SIOS
<Multi_key> <U11AB> <U11BD>		: "ᆬ"	U11ac # HANGUL JONGSEONG NIEUN-CIEUC
<Multi_key> <U11AB> <U11C2>		: "ᆭ"	U11ad # HANGUL JONGSEONG NIEUN-HIEUH
<Multi_key> <U11AF> <U11A8>		: "ᆰ"	U11b0 # HANGUL JONGSEONG RIEUL-KIYEOK
<Multi_key> <U11AF> <U11B7>		: "ᆱ"	U11b1 # HANGUL JONGSEONG RIEUL-MIEUM
<Multi_key> <U11AF> <U11B8>		: "ᆲ"	U11b2 # HANGUL JONGSEONG RIEUL-PIEUP
<Multi_key> <U11AF> <U11BA>		: "ᆳ"	U11b3 # HANGUL JONGSEONG RIEUL-SIOS
<Multi_key> <U11AF> <U11C0>		: "ᆴ"	U11b4 # HANGUL JONGSEONG RIEUL-THIEUTH
<Multi_key> <U11AF> <U11C1>		: "ᆵ"	U11b5 # HANGUL JONGSEONG RIEUL-PHIEUPH
<Multi_key> <U11AF> <U11C2>		: "ᆶ"	U11b6 # HANGUL JONGSEONG RIEUL-HIEUH
<Multi_key> <U11B8> <U11BA>		: "ᆹ"	U11b9 # HANGUL JONGSEONG PIEUP-SIOS
<Multi_key> <U11BA> <U11BA>		: "ᆻ"	U11bb # HANGUL JONGSEONG SSANGSIOS
<Multi_key> <U11A8> <U11AF>		: "ᇃ"	U11c3 # HANGUL JONGSEONG KIYEOK-RIEUL
<Multi_key> <U11AB> <U11A8>		: "ᇅ"	U11c5 # HANGUL JONGSEONG NIEUN-KIYEOK
<Multi_key> <U11AB> <U11AE>		: "ᇆ"	U11c6 # HANGUL JONGSEONG NIEUN-TIKEUT
<Multi_key> <U11AB> <U11BA>		: "ᇇ"	U11c7 # HANGUL JONGSEONG NIEUN-SIOS
<Multi_key> <U11AB> <U11EB>		: "ᇈ"	U11c8 # HANGUL JONGSEONG NIEUN-PANSIOS
<Multi_key> <U11AB> <U11C0>		: "ᇉ"	U11c9 # HANGUL JONGSEONG NIEUN-THIEUTH
<Multi_key> <U11AE> <U11A8>		: "ᇊ"	U11ca # HANGUL JONGSEONG TIKEUT-KIYEOK
<Multi_key> <U11AE> <U11AF>		: "ᇋ"	U11cb # HANGUL JONGSEONG TIKEUT-RIEUL
<Multi_key> <U11AF> <U11AB>		: "ᇍ"	U11cd # HANGUL JONGSEONG RIEUL-NIEUN
<Multi_key> <U11AF> <U11AE>		: "ᇎ"	U11ce # HANGUL JONGSEONG RIEUL-TIKEUT
<Multi_key> <U11AF> <U11AF>		: "ᇐ"	U11d0 # HANGUL JONGSEONG SSANGRIEUL
<Multi_key> <U11AF> <U11EB>		: "ᇗ"	U11d7 # HANGUL JONGSEONG RIEUL-PANSIOS
<Multi_key> <U11AF> <U11BF>		: "ᇘ"	U11d8 # HANGUL JONGSEONG RIEUL-KHIEUKH
<Multi_key> <U11AF> <U11F9>		: "ᇙ"	U11d9 # HANGUL JONGSEONG RIEUL-YEORINHIEUH
<Multi_key> <U11B7> <U11A8>		: "ᇚ"	U11da # HANGUL JONGSEONG MIEUM-KIYEOK
<Multi_key> <U11B7> <U11AF>		: "ᇛ"	U11db # HANGUL JONGSEONG MIEUM-RIEUL
<Multi_key> <U11B7> <U11B8>		: "ᇜ"	U11dc # HANGUL JONGSEONG MIEUM-PIEUP
<Multi_key> <U11B7> <U11BA>		: "ᇝ"	U11dd # HANGUL JONGSEONG MIEUM-SIOS
<Multi_key> <U11B7> <U11EB>		: "ᇟ"	U11df # HANGUL JONGSEONG MIEUM-PANSIOS
<Multi_key> <U11B7> <U11BE>		: "ᇠ"	U11e0 # HANGUL JONGSEONG MIEUM-CHIEUCH
<Multi_key> <U11B7> <U11C2>		: "ᇡ"	U11e1 # HANGUL JONGSEONG MIEUM-HIEUH
<Multi_key> <U11B7> <U11BC>		: "ᇢ"	U11e2 # HANGUL JONGSEONG KAPYEOUNMIEUM
<Multi_key> <U11B8> <U11AF>		: "ᇣ"	U11e3 # HANGUL JONGSEONG PIEUP-RIEUL
<Multi_key> <U11B8> <U11C1>		: "ᇤ"	U11e4 # HANGUL JONGSEONG PIEUP-PHIEUPH
<Multi_key> <U11B8> <U11C2>		: "ᇥ"	U11e5 # HANGUL JONGSEONG PIEUP-HIEUH
<Multi_key> <U11B8> <U11BC>		: "ᇦ"	U11e6 # HANGUL JONGSEONG KAPYEOUNPIEUP
<Multi_key> <U11BA> <U11A8>		: "ᇧ"	U11e7 # HANGUL JONGSEONG SIOS-KIYEOK
<Multi_key> <U11BA> <U11AE>		: "ᇨ"	U11e8 # HANGUL JONGSEONG SIOS-TIKEUT
<Multi_key> <U11BA> <U11AF>		: "ᇩ"	U11e9 # HANGUL JONGSEONG SIOS-RIEUL
<Multi_key> <U11BA> <U11B8>		: "ᇪ"	U11ea # HANGUL JONGSEONG SIOS-PIEUP
<Multi_key> <U11BC> <U11A8>		: "ᇬ"	U11ec # HANGUL JONGSEONG IEUNG-KIYEOK
<Multi_key> <U11BC> <U11BC>		: "ᇮ"	U11ee # HANGUL JONGSEONG SSANGIEUNG
<Multi_key> <U11BC> <U11BF>		: "ᇯ"	U11ef # HANGUL JONGSEONG IEUNG-KHIEUKH
<Multi_key> <U11F0> <U11BA>		: "ᇱ"	U11f1 # HANGUL JONGSEONG YESIEUNG-SIOS
<Multi_key> <U11F0> <U11EB>		: "ᇲ"	U11f2 # HANGUL JONGSEONG YESIEUNG-PANSIOS
<Multi_key> <U11C1> <U11B8>		: "ᇳ"	U11f3 # HANGUL JONGSEONG PHIEUPH-PIEUP
<Multi_key> <U11C1> <U11BC>		: "ᇴ"	U11f4 # HANGUL JONGSEONG KAPYEOUNPHIEUPH
<Multi_key> <U11C2> <U11AB>		: "ᇵ"	U11f5 # HANGUL JONGSEONG HIEUH-NIEUN
<Multi_key> <U11C2> <U11AF>		: "ᇶ"	U11f6 # HANGUL JONGSEONG HIEUH-RIEUL
<Multi_key> <U11C2> <U11B7>		: "ᇷ"	U11f7 # HANGUL JONGSEONG HIEUH-MIEUM
<Multi_key> <U11C2> <U11B8>		: "ᇸ"	U11f8 # HANGUL JONGSEONG HIEUH-PIEUP
<Multi_key> <U1121> <U1100>		: "ᄢ"	U1122 # HANGUL CHOSEONG PIEUP-SIOS-KIYEOK
<Multi_key> <U1121> <U1103>		: "ᄣ"	U1123 # HANGUL CHOSEONG PIEUP-SIOS-TIKEUT
<Multi_key> <U1121> <U1107>		: "ᄤ"	U1124 # HANGUL CHOSEONG PIEUP-SIOS-PIEUP
<Multi_key> <U1121> <U1109>		: "ᄥ"	U1125 # HANGUL CHOSEONG PIEUP-SSANGSIOS
<Multi_key> <U1121> <U110C>		: "ᄦ"	U1126 # HANGUL CHOSEONG PIEUP-SIOS-CIEUC
<Multi_key> <U1108> <U110B>		: "ᄬ"	U112c # HANGUL CHOSEONG KAPYEOUNSSANGPIEUP
<Multi_key> <U1132> <U1100>		: "ᄳ"	U1133 # HANGUL CHOSEONG SIOS-PIEUP-KIYEOK
<Multi_key> <U110A> <U1109>		: "ᄴ"	U1134 # HANGUL CHOSEONG SIOS-SSANGSIOS
<Multi_key> <U116A> <U1175>		: "ᅫ"	U116b # HANGUL JUNGSEONG WAE
<Multi_key> <U116F> <U1175>		: "ᅰ"	U1170 # HANGUL JUNGSEONG WE
<Multi_key> <U116F> <U1173>		: "ᆋ"	U118b # HANGUL JUNGSEONG U-EO-EU
<Multi_key> <U11AA> <U11A8>		: "ᇄ"	U11c4 # HANGUL JONGSEONG KIYEOK-SIOS-KIYEOK
<Multi_key> <U11B0> <U11BA>		: "ᇌ"	U11cc # HANGUL JONGSEONG RIEUL-KIYEOK-SIOS
<Multi_key> <U11CE> <U11C2>		: "ᇏ"	U11cf # HANGUL JONGSEONG RIEUL-TIKEUT-HIEUH
<Multi_key> <U11B1> <U11A8>		: "ᇑ"	U11d1 # HANGUL JONGSEONG RIEUL-MIEUM-KIYEOK
<Multi_key> <U11B1> <U11BA>		: "ᇒ"	U11d2 # HANGUL JONGSEONG RIEUL-MIEUM-SIOS
<Multi_key> <U11B2> <U11BA>		: "ᇓ"	U11d3 # HANGUL JONGSEONG RIEUL-PIEUP-SIOS
<Multi_key> <U11B2> <U11C2>		: "ᇔ"	U11d4 # HANGUL JONGSEONG RIEUL-PIEUP-HIEUH
<Multi_key> <U11B2> <U11BC>		: "ᇕ"	U11d5 # HANGUL JONGSEONG RIEUL-KAPYEOUNPIEUP
<Multi_key> <U11B3> <U11BA>		: "ᇖ"	U11d6 # HANGUL JONGSEONG RIEUL-SSANGSIOS
<Multi_key> <U11DD> <U11BA>		: "ᇞ"	U11de # HANGUL JONGSEONG MIEUM-SSANGSIOS
<Multi_key> <U11EC> <U11A8>		: "ᇭ"	U11ed # HANGUL JONGSEONG IEUNG-SSANGKIYEOK
<Multi_key> <U1107> <U112D>		: "ᄢ"	U1122 # HANGUL CHOSEONG PIEUP-SIOS-KIYEOK
<Multi_key> <U1107> <U112F>		: "ᄣ"	U1123 # HANGUL CHOSEONG PIEUP-SIOS-TIKEUT
<Multi_key> <U1107> <U1132>		: "ᄤ"	U1124 # HANGUL CHOSEONG PIEUP-SIOS-PIEUP
<Multi_key> <U1107> <U110A>		: "ᄥ"	U1125 # HANGUL CHOSEONG PIEUP-SSANGSIOS
<Multi_key> <U1107> <U1136>		: "ᄦ"	U1126 # HANGUL CHOSEONG PIEUP-SIOS-CIEUC
<Multi_key> <U1107> <U112B>		: "ᄬ"	U112c # HANGUL CHOSEONG KAPYEOUNSSANGPIEUP
<Multi_key> <U1109> <U111E>		: "ᄳ"	U1133 # HANGUL CHOSEONG SIOS-PIEUP-KIYEOK
<Multi_key> <U1109> <U110A>		: "ᄴ"	U1134 # HANGUL CHOSEONG SIOS-SSANGSIOS
<Multi_key> <U1169> <U1162>		: "ᅫ"	U116b # HANGUL JUNGSEONG WAE
<Multi_key> <U116E> <U1166>		: "ᅰ"	U1170 # HANGUL JUNGSEONG WE
<Multi_key> <U116E> <U117C>		: "ᆋ"	U118b # HANGUL JUNGSEONG U-EO-EU
<Multi_key> <U11A8> <U11E7>		: "ᇄ"	U11c4 # HANGUL JONGSEONG KIYEOK-SIOS-KIYEOK
<Multi_key> <U11AF> <U11AA>		: "ᇌ"	U11cc # HANGUL JONGSEONG RIEUL-KIYEOK-SIOS
<Multi_key> <U11AF> <U11DA>		: "ᇑ"	U11d1 # HANGUL JONGSEONG RIEUL-MIEUM-KIYEOK
<Multi_key> <U11AF> <U11DD>		: "ᇒ"	U11d2 # HANGUL JONGSEONG RIEUL-MIEUM-SIOS
<Multi_key> <U11AF> <U11B9>		: "ᇓ"	U11d3 # HANGUL JONGSEONG RIEUL-PIEUP-SIOS
<Multi_key> <U11AF> <U11E5>		: "ᇔ"	U11d4 # HANGUL JONGSEONG RIEUL-PIEUP-HIEUH
<Multi_key> <U11AF> <U11E6>		: "ᇕ"	U11d5 # HANGUL JONGSEONG RIEUL-KAPYEOUNPIEUP
<Multi_key> <U11AF> <U11BB>		: "ᇖ"	U11d6 # HANGUL JONGSEONG RIEUL-SSANGSIOS
<Multi_key> <U11B7> <U11BB>		: "ᇞ"	U11de # HANGUL JONGSEONG MIEUM-SSANGSIOS
<Multi_key> <U11BC> <U11A9>		: "ᇭ"	U11ed # HANGUL JONGSEONG IEUNG-SSANGKIYEOK
# Latin Extended Additional
<dead_belowring> <A>				: "Ḁ"	U1E00 # LATIN CAPITAL LETTER A WITH RING BELOW
<dead_belowring> <a>				: "ḁ"	U1E01 # LATIN SMALL LETTER A WITH RING BELOW
<dead_abovedot> <B>				: "Ḃ"	U1E02 # LATIN CAPITAL LETTER B WITH DOT ABOVE
<Multi_key> <period> <B>			: "Ḃ"	U1E02 # LATIN CAPITAL LETTER B WITH DOT ABOVE
<Multi_key> <B> <period>			: "Ḃ"	U1E02 # LATIN CAPITAL LETTER B WITH DOT ABOVE
<dead_abovedot> <b>				: "ḃ"	U1E03 # LATIN SMALL LETTER B WITH DOT ABOVE
<Multi_key> <period> <b>			: "ḃ"	U1E03 # LATIN SMALL LETTER B WITH DOT ABOVE
<Multi_key> <b> <period>			: "ḃ"	U1E03 # LATIN SMALL LETTER B WITH DOT ABOVE
<dead_belowdot> <B>				: "Ḅ"	U1E04 # LATIN CAPITAL LETTER B WITH DOT BELOW
<Multi_key> <exclam> <B>			: "Ḅ"	U1E04 # LATIN CAPITAL LETTER B WITH DOT BELOW
<dead_belowdot> <b>				: "ḅ"	U1E05 # LATIN SMALL LETTER B WITH DOT BELOW
<Multi_key> <exclam> <b>			: "ḅ"	U1E05 # LATIN SMALL LETTER B WITH DOT BELOW
<dead_belowmacron> <B>				: "Ḇ"	U1E06 # LATIN CAPITAL LETTER B WITH LINE BELOW
<dead_belowmacron> <b>				: "ḇ"	U1E07 # LATIN SMALL LETTER B WITH LINE BELOW
<dead_acute> <Ccedilla>				: "Ḉ"	U1E08 # LATIN CAPITAL LETTER C WITH CEDILLA AND ACUTE
<Multi_key> <acute> <Ccedilla>			: "Ḉ"	U1E08 # LATIN CAPITAL LETTER C WITH CEDILLA AND ACUTE
<Multi_key> <apostrophe> <Ccedilla>		: "Ḉ"	U1E08 # LATIN CAPITAL LETTER C WITH CEDILLA AND ACUTE
<dead_acute> <dead_cedilla> <C>			: "Ḉ"	U1E08 # LATIN CAPITAL LETTER C WITH CEDILLA AND ACUTE
<dead_acute> <Multi_key> <comma> <C>		: "Ḉ"	U1E08 # LATIN CAPITAL LETTER C WITH CEDILLA AND ACUTE
<dead_acute> <Multi_key> <cedilla> <C>		: "Ḉ"	U1E08 # LATIN CAPITAL LETTER C WITH CEDILLA AND ACUTE
<Multi_key> <acute> <dead_cedilla> <C>		: "Ḉ"	U1E08 # LATIN CAPITAL LETTER C WITH CEDILLA AND ACUTE
<Multi_key> <acute> <comma> <C>			: "Ḉ"	U1E08 # LATIN CAPITAL LETTER C WITH CEDILLA AND ACUTE
<Multi_key> <acute> <cedilla> <C>		: "Ḉ"	U1E08 # LATIN CAPITAL LETTER C WITH CEDILLA AND ACUTE
<Multi_key> <apostrophe> <dead_cedilla> <C>	: "Ḉ"	U1E08 # LATIN CAPITAL LETTER C WITH CEDILLA AND ACUTE
<Multi_key> <apostrophe> <cedilla> <C>		: "Ḉ"	U1E08 # LATIN CAPITAL LETTER C WITH CEDILLA AND ACUTE
<dead_acute> <ccedilla>				: "ḉ"	U1E09 # LATIN SMALL LETTER C WITH CEDILLA AND ACUTE
<Multi_key> <acute> <ccedilla>			: "ḉ"	U1E09 # LATIN SMALL LETTER C WITH CEDILLA AND ACUTE
<Multi_key> <apostrophe> <ccedilla>		: "ḉ"	U1E09 # LATIN SMALL LETTER C WITH CEDILLA AND ACUTE
<dead_acute> <dead_cedilla> <c>			: "ḉ"	U1E09 # LATIN SMALL LETTER C WITH CEDILLA AND ACUTE
<dead_acute> <Multi_key> <comma> <c>		: "ḉ"	U1E09 # LATIN SMALL LETTER C WITH CEDILLA AND ACUTE
<dead_acute> <Multi_key> <cedilla> <c>		: "ḉ"	U1E09 # LATIN SMALL LETTER C WITH CEDILLA AND ACUTE
<Multi_key> <acute> <dead_cedilla> <c>		: "ḉ"	U1E09 # LATIN SMALL LETTER C WITH CEDILLA AND ACUTE
<Multi_key> <acute> <comma> <c>			: "ḉ"	U1E09 # LATIN SMALL LETTER C WITH CEDILLA AND ACUTE
<Multi_key> <acute> <cedilla> <c>		: "ḉ"	U1E09 # LATIN SMALL LETTER C WITH CEDILLA AND ACUTE
<Multi_key> <apostrophe> <dead_cedilla> <c>	: "ḉ"	U1E09 # LATIN SMALL LETTER C WITH CEDILLA AND ACUTE
<Multi_key> <apostrophe> <cedilla> <c>		: "ḉ"	U1E09 # LATIN SMALL LETTER C WITH CEDILLA AND ACUTE
<dead_abovedot> <D>				: "Ḋ"	U1E0A # LATIN CAPITAL LETTER D WITH DOT ABOVE
<Multi_key> <period> <D>			: "Ḋ"	U1E0A # LATIN CAPITAL LETTER D WITH DOT ABOVE
<Multi_key> <D> <period>			: "Ḋ"	U1E0A # LATIN CAPITAL LETTER D WITH DOT ABOVE
<dead_abovedot> <d>				: "ḋ"	U1E0B # LATIN SMALL LETTER D WITH DOT ABOVE
<Multi_key> <period> <d>			: "ḋ"	U1E0B # LATIN SMALL LETTER D WITH DOT ABOVE
<Multi_key> <d> <period>			: "ḋ"	U1E0B # LATIN SMALL LETTER D WITH DOT ABOVE
<dead_belowdot> <D>				: "Ḍ"	U1E0C # LATIN CAPITAL LETTER D WITH DOT BELOW
<Multi_key> <exclam> <D>			: "Ḍ"	U1E0C # LATIN CAPITAL LETTER D WITH DOT BELOW
<dead_belowdot> <d>				: "ḍ"	U1E0D # LATIN SMALL LETTER D WITH DOT BELOW
<Multi_key> <exclam> <d>			: "ḍ"	U1E0D # LATIN SMALL LETTER D WITH DOT BELOW
<dead_belowmacron> <D>				: "Ḏ"	U1E0E # LATIN CAPITAL LETTER D WITH LINE BELOW
<dead_belowmacron> <d>				: "ḏ"	U1E0F # LATIN SMALL LETTER D WITH LINE BELOW
<dead_cedilla> <D>				: "Ḑ"	U1E10 # LATIN CAPITAL LETTER D WITH CEDILLA
<Multi_key> <comma> <D>				: "Ḑ"	U1E10 # LATIN CAPITAL LETTER D WITH CEDILLA
<Multi_key> <D> <comma>				: "Ḑ"	U1E10 # LATIN CAPITAL LETTER D WITH CEDILLA
<Multi_key> <cedilla> <D>			: "Ḑ"	U1E10 # LATIN CAPITAL LETTER D WITH CEDILLA
<dead_cedilla> <d>				: "ḑ"	U1E11 # LATIN SMALL LETTER D WITH CEDILLA
<Multi_key> <comma> <d>				: "ḑ"	U1E11 # LATIN SMALL LETTER D WITH CEDILLA
<Multi_key> <d> <comma>				: "ḑ"	U1E11 # LATIN SMALL LETTER D WITH CEDILLA
<Multi_key> <cedilla> <d>			: "ḑ"	U1E11 # LATIN SMALL LETTER D WITH CEDILLA
<dead_belowcircumflex> <D>			: "Ḓ"	U1E12 # LATIN CAPITAL LETTER D WITH CIRCUMFLEX BELOW
<dead_belowcircumflex> <d>			: "ḓ"	U1E13 # LATIN SMALL LETTER D WITH CIRCUMFLEX BELOW
<dead_grave> <Emacron>				: "Ḕ"	U1E14 # LATIN CAPITAL LETTER E WITH MACRON AND GRAVE
<Multi_key> <grave> <Emacron>			: "Ḕ"	U1E14 # LATIN CAPITAL LETTER E WITH MACRON AND GRAVE
<dead_grave> <dead_macron> <E>			: "Ḕ"	U1E14 # LATIN CAPITAL LETTER E WITH MACRON AND GRAVE
<dead_grave> <Multi_key> <macron> <E>		: "Ḕ"	U1E14 # LATIN CAPITAL LETTER E WITH MACRON AND GRAVE
<dead_grave> <Multi_key> <underscore> <E>	: "Ḕ"	U1E14 # LATIN CAPITAL LETTER E WITH MACRON AND GRAVE
<Multi_key> <grave> <dead_macron> <E>		: "Ḕ"	U1E14 # LATIN CAPITAL LETTER E WITH MACRON AND GRAVE
<Multi_key> <grave> <macron> <E>		: "Ḕ"	U1E14 # LATIN CAPITAL LETTER E WITH MACRON AND GRAVE
<Multi_key> <grave> <underscore> <E>		: "Ḕ"	U1E14 # LATIN CAPITAL LETTER E WITH MACRON AND GRAVE
<dead_grave> <emacron>				: "ḕ"	U1E15 # LATIN SMALL LETTER E WITH MACRON AND GRAVE
<Multi_key> <grave> <emacron>			: "ḕ"	U1E15 # LATIN SMALL LETTER E WITH MACRON AND GRAVE
<dead_grave> <dead_macron> <e>			: "ḕ"	U1E15 # LATIN SMALL LETTER E WITH MACRON AND GRAVE
<dead_grave> <Multi_key> <macron> <e>		: "ḕ"	U1E15 # LATIN SMALL LETTER E WITH MACRON AND GRAVE
<dead_grave> <Multi_key> <underscore> <e>	: "ḕ"	U1E15 # LATIN SMALL LETTER E WITH MACRON AND GRAVE
<Multi_key> <grave> <dead_macron> <e>		: "ḕ"	U1E15 # LATIN SMALL LETTER E WITH MACRON AND GRAVE
<Multi_key> <grave> <macron> <e>		: "ḕ"	U1E15 # LATIN SMALL LETTER E WITH MACRON AND GRAVE
<Multi_key> <grave> <underscore> <e>		: "ḕ"	U1E15 # LATIN SMALL LETTER E WITH MACRON AND GRAVE
<dead_acute> <Emacron>				: "Ḗ"	U1E16 # LATIN CAPITAL LETTER E WITH MACRON AND ACUTE
<Multi_key> <acute> <Emacron>			: "Ḗ"	U1E16 # LATIN CAPITAL LETTER E WITH MACRON AND ACUTE
<Multi_key> <apostrophe> <Emacron>		: "Ḗ"	U1E16 # LATIN CAPITAL LETTER E WITH MACRON AND ACUTE
<dead_acute> <dead_macron> <E>			: "Ḗ"	U1E16 # LATIN CAPITAL LETTER E WITH MACRON AND ACUTE
<dead_acute> <Multi_key> <macron> <E>		: "Ḗ"	U1E16 # LATIN CAPITAL LETTER E WITH MACRON AND ACUTE
<dead_acute> <Multi_key> <underscore> <E>	: "Ḗ"	U1E16 # LATIN CAPITAL LETTER E WITH MACRON AND ACUTE
<Multi_key> <acute> <dead_macron> <E>		: "Ḗ"	U1E16 # LATIN CAPITAL LETTER E WITH MACRON AND ACUTE
<Multi_key> <acute> <macron> <E>		: "Ḗ"	U1E16 # LATIN CAPITAL LETTER E WITH MACRON AND ACUTE
<Multi_key> <acute> <underscore> <E>		: "Ḗ"	U1E16 # LATIN CAPITAL LETTER E WITH MACRON AND ACUTE
<Multi_key> <apostrophe> <dead_macron> <E>	: "Ḗ"	U1E16 # LATIN CAPITAL LETTER E WITH MACRON AND ACUTE
<Multi_key> <apostrophe> <macron> <E>		: "Ḗ"	U1E16 # LATIN CAPITAL LETTER E WITH MACRON AND ACUTE
<Multi_key> <apostrophe> <underscore> <E>	: "Ḗ"	U1E16 # LATIN CAPITAL LETTER E WITH MACRON AND ACUTE
<dead_acute> <emacron>				: "ḗ"	U1E17 # LATIN SMALL LETTER E WITH MACRON AND ACUTE
<Multi_key> <acute> <emacron>			: "ḗ"	U1E17 # LATIN SMALL LETTER E WITH MACRON AND ACUTE
<Multi_key> <apostrophe> <emacron>		: "ḗ"	U1E17 # LATIN SMALL LETTER E WITH MACRON AND ACUTE
<dead_acute> <dead_macron> <e>			: "ḗ"	U1E17 # LATIN SMALL LETTER E WITH MACRON AND ACUTE
<dead_acute> <Multi_key> <macron> <e>		: "ḗ"	U1E17 # LATIN SMALL LETTER E WITH MACRON AND ACUTE
<dead_acute> <Multi_key> <underscore> <e>	: "ḗ"	U1E17 # LATIN SMALL LETTER E WITH MACRON AND ACUTE
<Multi_key> <acute> <dead_macron> <e>		: "ḗ"	U1E17 # LATIN SMALL LETTER E WITH MACRON AND ACUTE
<Multi_key> <acute> <macron> <e>		: "ḗ"	U1E17 # LATIN SMALL LETTER E WITH MACRON AND ACUTE
<Multi_key> <acute> <underscore> <e>		: "ḗ"	U1E17 # LATIN SMALL LETTER E WITH MACRON AND ACUTE
<Multi_key> <apostrophe> <dead_macron> <e>	: "ḗ"	U1E17 # LATIN SMALL LETTER E WITH MACRON AND ACUTE
<Multi_key> <apostrophe> <macron> <e>		: "ḗ"	U1E17 # LATIN SMALL LETTER E WITH MACRON AND ACUTE
<Multi_key> <apostrophe> <underscore> <e>	: "ḗ"	U1E17 # LATIN SMALL LETTER E WITH MACRON AND ACUTE
<dead_belowcircumflex> <E>			: "Ḙ"	U1E18 # LATIN CAPITAL LETTER E WITH CIRCUMFLEX BELOW
<dead_belowcircumflex> <e>			: "ḙ"	U1E19 # LATIN SMALL LETTER E WITH CIRCUMFLEX BELOW
<dead_belowtilde> <E>				: "Ḛ"	U1E1A # LATIN CAPITAL LETTER E WITH TILDE BELOW
<dead_belowtilde> <e>				: "ḛ"	U1E1B # LATIN SMALL LETTER E WITH TILDE BELOW
<dead_breve> <dead_cedilla> <E>			: "Ḝ"	U1E1C # LATIN CAPITAL LETTER E WITH CEDILLA AND BREVE
<dead_breve> <Multi_key> <comma> <E>		: "Ḝ"	U1E1C # LATIN CAPITAL LETTER E WITH CEDILLA AND BREVE
<dead_breve> <Multi_key> <cedilla> <E>		: "Ḝ"	U1E1C # LATIN CAPITAL LETTER E WITH CEDILLA AND BREVE
<Multi_key> <U> <dead_cedilla> <E>		: "Ḝ"	U1E1C # LATIN CAPITAL LETTER E WITH CEDILLA AND BREVE
<Multi_key> <U> <space> <comma> <E>		: "Ḝ"	U1E1C # LATIN CAPITAL LETTER E WITH CEDILLA AND BREVE
<Multi_key> <U> <cedilla> <E>			: "Ḝ"	U1E1C # LATIN CAPITAL LETTER E WITH CEDILLA AND BREVE
<Multi_key> <b> <dead_cedilla> <E>		: "Ḝ"	U1E1C # LATIN CAPITAL LETTER E WITH CEDILLA AND BREVE
<Multi_key> <b> <comma> <E>			: "Ḝ"	U1E1C # LATIN CAPITAL LETTER E WITH CEDILLA AND BREVE
<Multi_key> <b> <cedilla> <E>			: "Ḝ"	U1E1C # LATIN CAPITAL LETTER E WITH CEDILLA AND BREVE
<dead_breve> <dead_cedilla> <e>			: "ḝ"	U1E1D # LATIN SMALL LETTER E WITH CEDILLA AND BREVE
<dead_breve> <Multi_key> <comma> <e>		: "ḝ"	U1E1D # LATIN SMALL LETTER E WITH CEDILLA AND BREVE
<dead_breve> <Multi_key> <cedilla> <e>		: "ḝ"	U1E1D # LATIN SMALL LETTER E WITH CEDILLA AND BREVE
<Multi_key> <U> <dead_cedilla> <e>		: "ḝ"	U1E1D # LATIN SMALL LETTER E WITH CEDILLA AND BREVE
<Multi_key> <U> <space> <comma> <e>		: "ḝ"	U1E1D # LATIN SMALL LETTER E WITH CEDILLA AND BREVE
<Multi_key> <U> <cedilla> <e>			: "ḝ"	U1E1D # LATIN SMALL LETTER E WITH CEDILLA AND BREVE
<Multi_key> <b> <dead_cedilla> <e>		: "ḝ"	U1E1D # LATIN SMALL LETTER E WITH CEDILLA AND BREVE
<Multi_key> <b> <comma> <e>			: "ḝ"	U1E1D # LATIN SMALL LETTER E WITH CEDILLA AND BREVE
<Multi_key> <b> <cedilla> <e>			: "ḝ"	U1E1D # LATIN SMALL LETTER E WITH CEDILLA AND BREVE
<dead_abovedot> <F>				: "Ḟ"	U1E1E # LATIN CAPITAL LETTER F WITH DOT ABOVE
<Multi_key> <period> <F>			: "Ḟ"	U1E1E # LATIN CAPITAL LETTER F WITH DOT ABOVE
<Multi_key> <F> <period>			: "Ḟ"	U1E1E # LATIN CAPITAL LETTER F WITH DOT ABOVE
<dead_abovedot> <f>				: "ḟ"	U1E1F # LATIN SMALL LETTER F WITH DOT ABOVE
<Multi_key> <period> <f>			: "ḟ"	U1E1F # LATIN SMALL LETTER F WITH DOT ABOVE
<Multi_key> <f> <period>			: "ḟ"	U1E1F # LATIN SMALL LETTER F WITH DOT ABOVE
<dead_macron> <G>				: "Ḡ"	U1E20 # LATIN CAPITAL LETTER G WITH MACRON
<Multi_key> <macron> <G>			: "Ḡ"	U1E20 # LATIN CAPITAL LETTER G WITH MACRON
<Multi_key> <underscore> <G>			: "Ḡ"	U1E20 # LATIN CAPITAL LETTER G WITH MACRON
<dead_macron> <g>				: "ḡ"	U1E21 # LATIN SMALL LETTER G WITH MACRON
<Multi_key> <macron> <g>			: "ḡ"	U1E21 # LATIN SMALL LETTER G WITH MACRON
<Multi_key> <underscore> <g>			: "ḡ"	U1E21 # LATIN SMALL LETTER G WITH MACRON
<dead_abovedot> <H>				: "Ḣ"	U1E22 # LATIN CAPITAL LETTER H WITH DOT ABOVE
<Multi_key> <period> <H>			: "Ḣ"	U1E22 # LATIN CAPITAL LETTER H WITH DOT ABOVE
<dead_abovedot> <h>				: "ḣ"	U1E23 # LATIN SMALL LETTER H WITH DOT ABOVE
<Multi_key> <period> <h>			: "ḣ"	U1E23 # LATIN SMALL LETTER H WITH DOT ABOVE
<dead_belowdot> <H>				: "Ḥ"	U1E24 # LATIN CAPITAL LETTER H WITH DOT BELOW
<Multi_key> <exclam> <H>			: "Ḥ"	U1E24 # LATIN CAPITAL LETTER H WITH DOT BELOW
<dead_belowdot> <h>				: "ḥ"	U1E25 # LATIN SMALL LETTER H WITH DOT BELOW
<Multi_key> <exclam> <h>			: "ḥ"	U1E25 # LATIN SMALL LETTER H WITH DOT BELOW
<dead_diaeresis> <H>				: "Ḧ"	U1E26 # LATIN CAPITAL LETTER H WITH DIAERESIS
<Multi_key> <quotedbl> <H>			: "Ḧ"	U1E26 # LATIN CAPITAL LETTER H WITH DIAERESIS
<dead_diaeresis> <h>				: "ḧ"	U1E27 # LATIN SMALL LETTER H WITH DIAERESIS
<Multi_key> <quotedbl> <h>			: "ḧ"	U1E27 # LATIN SMALL LETTER H WITH DIAERESIS
<dead_cedilla> <H>				: "Ḩ"	U1E28 # LATIN CAPITAL LETTER H WITH CEDILLA
<Multi_key> <comma> <H>				: "Ḩ"	U1E28 # LATIN CAPITAL LETTER H WITH CEDILLA
<Multi_key> <H> <comma>				: "Ḩ"	U1E28 # LATIN CAPITAL LETTER H WITH CEDILLA
<Multi_key> <cedilla> <H>			: "Ḩ"	U1E28 # LATIN CAPITAL LETTER H WITH CEDILLA
<dead_cedilla> <h>				: "ḩ"	U1E29 # LATIN SMALL LETTER H WITH CEDILLA
<Multi_key> <comma> <h>				: "ḩ"	U1E29 # LATIN SMALL LETTER H WITH CEDILLA
<Multi_key> <h> <comma>				: "ḩ"	U1E29 # LATIN SMALL LETTER H WITH CEDILLA
<Multi_key> <cedilla> <h>			: "ḩ"	U1E29 # LATIN SMALL LETTER H WITH CEDILLA
<dead_belowbreve> <H>				: "Ḫ"	U1E2A # LATIN CAPITAL LETTER H WITH BREVE BELOW
<dead_belowbreve> <h>				: "ḫ"	U1E2B # LATIN SMALL LETTER H WITH BREVE BELOW
<dead_belowtilde> <I>				: "Ḭ"	U1E2C # LATIN CAPITAL LETTER I WITH TILDE BELOW
<dead_belowtilde> <i>				: "ḭ"	U1E2D # LATIN SMALL LETTER I WITH TILDE BELOW
<dead_acute> <Idiaeresis>			: "Ḯ"	U1E2E # LATIN CAPITAL LETTER I WITH DIAERESIS AND ACUTE
<Multi_key> <acute> <Idiaeresis>		: "Ḯ"	U1E2E # LATIN CAPITAL LETTER I WITH DIAERESIS AND ACUTE
<Multi_key> <apostrophe> <Idiaeresis>		: "Ḯ"	U1E2E # LATIN CAPITAL LETTER I WITH DIAERESIS AND ACUTE
<dead_acute> <dead_diaeresis> <I>		: "Ḯ"	U1E2E # LATIN CAPITAL LETTER I WITH DIAERESIS AND ACUTE
<dead_acute> <Multi_key> <quotedbl> <I>		: "Ḯ"	U1E2E # LATIN CAPITAL LETTER I WITH DIAERESIS AND ACUTE
<Multi_key> <acute> <dead_diaeresis> <I>	: "Ḯ"	U1E2E # LATIN CAPITAL LETTER I WITH DIAERESIS AND ACUTE
<Multi_key> <acute> <quotedbl> <I>		: "Ḯ"	U1E2E # LATIN CAPITAL LETTER I WITH DIAERESIS AND ACUTE
<Multi_key> <apostrophe> <dead_diaeresis> <I>	: "Ḯ"	U1E2E # LATIN CAPITAL LETTER I WITH DIAERESIS AND ACUTE
<Multi_key> <apostrophe> <quotedbl> <I>		: "Ḯ"	U1E2E # LATIN CAPITAL LETTER I WITH DIAERESIS AND ACUTE
<dead_acute> <idiaeresis>			: "ḯ"	U1E2F # LATIN SMALL LETTER I WITH DIAERESIS AND ACUTE
<Multi_key> <acute> <idiaeresis>		: "ḯ"	U1E2F # LATIN SMALL LETTER I WITH DIAERESIS AND ACUTE
<Multi_key> <apostrophe> <idiaeresis>		: "ḯ"	U1E2F # LATIN SMALL LETTER I WITH DIAERESIS AND ACUTE
<dead_acute> <dead_diaeresis> <i>		: "ḯ"	U1E2F # LATIN SMALL LETTER I WITH DIAERESIS AND ACUTE
<dead_acute> <Multi_key> <quotedbl> <i>		: "ḯ"	U1E2F # LATIN SMALL LETTER I WITH DIAERESIS AND ACUTE
<Multi_key> <acute> <dead_diaeresis> <i>	: "ḯ"	U1E2F # LATIN SMALL LETTER I WITH DIAERESIS AND ACUTE
<Multi_key> <acute> <quotedbl> <i>		: "ḯ"	U1E2F # LATIN SMALL LETTER I WITH DIAERESIS AND ACUTE
<Multi_key> <apostrophe> <dead_diaeresis> <i>	: "ḯ"	U1E2F # LATIN SMALL LETTER I WITH DIAERESIS AND ACUTE
<Multi_key> <apostrophe> <quotedbl> <i>		: "ḯ"	U1E2F # LATIN SMALL LETTER I WITH DIAERESIS AND ACUTE
<dead_acute> <K>				: "Ḱ"	U1E30 # LATIN CAPITAL LETTER K WITH ACUTE
<Multi_key> <acute> <K>				: "Ḱ"	U1E30 # LATIN CAPITAL LETTER K WITH ACUTE
<Multi_key> <apostrophe> <K>			: "Ḱ"	U1E30 # LATIN CAPITAL LETTER K WITH ACUTE
<dead_acute> <k>				: "ḱ"	U1E31 # LATIN SMALL LETTER K WITH ACUTE
<Multi_key> <acute> <k>				: "ḱ"	U1E31 # LATIN SMALL LETTER K WITH ACUTE
<Multi_key> <apostrophe> <k>			: "ḱ"	U1E31 # LATIN SMALL LETTER K WITH ACUTE
<dead_belowdot> <K>				: "Ḳ"	U1E32 # LATIN CAPITAL LETTER K WITH DOT BELOW
<Multi_key> <exclam> <K>			: "Ḳ"	U1E32 # LATIN CAPITAL LETTER K WITH DOT BELOW
<dead_belowdot> <k>				: "ḳ"	U1E33 # LATIN SMALL LETTER K WITH DOT BELOW
<Multi_key> <exclam> <k>			: "ḳ"	U1E33 # LATIN SMALL LETTER K WITH DOT BELOW
<dead_belowmacron> <K>				: "Ḵ"	U1E34 # LATIN CAPITAL LETTER K WITH LINE BELOW
<dead_belowmacron> <k>				: "ḵ"	U1E35 # LATIN SMALL LETTER K WITH LINE BELOW
<dead_belowdot> <L>				: "Ḷ"	U1E36 # LATIN CAPITAL LETTER L WITH DOT BELOW
<Multi_key> <exclam> <L>			: "Ḷ"	U1E36 # LATIN CAPITAL LETTER L WITH DOT BELOW
<dead_belowdot> <l>				: "ḷ"	U1E37 # LATIN SMALL LETTER L WITH DOT BELOW
<Multi_key> <exclam> <l>			: "ḷ"	U1E37 # LATIN SMALL LETTER L WITH DOT BELOW
<dead_macron> <U1E36>				: "Ḹ"	U1E38 # LATIN CAPITAL LETTER L WITH DOT BELOW AND MACRON
<Multi_key> <macron> <U1E36>			: "Ḹ"	U1E38 # LATIN CAPITAL LETTER L WITH DOT BELOW AND MACRON
<Multi_key> <underscore> <U1E36>		: "Ḹ"	U1E38 # LATIN CAPITAL LETTER L WITH DOT BELOW AND MACRON
<dead_macron> <dead_belowdot> <L>		: "Ḹ"	U1E38 # LATIN CAPITAL LETTER L WITH DOT BELOW AND MACRON
<dead_macron> <Multi_key> <exclam> <L>		: "Ḹ"	U1E38 # LATIN CAPITAL LETTER L WITH DOT BELOW AND MACRON
<Multi_key> <macron> <dead_belowdot> <L>	: "Ḹ"	U1E38 # LATIN CAPITAL LETTER L WITH DOT BELOW AND MACRON
<Multi_key> <macron> <exclam> <L>		: "Ḹ"	U1E38 # LATIN CAPITAL LETTER L WITH DOT BELOW AND MACRON
<Multi_key> <underscore> <dead_belowdot> <L>	: "Ḹ"	U1E38 # LATIN CAPITAL LETTER L WITH DOT BELOW AND MACRON
<Multi_key> <underscore> <exclam> <L>		: "Ḹ"	U1E38 # LATIN CAPITAL LETTER L WITH DOT BELOW AND MACRON
<dead_macron> <U1E37>				: "ḹ"	U1E39 # LATIN SMALL LETTER L WITH DOT BELOW AND MACRON
<Multi_key> <macron> <U1E37>			: "ḹ"	U1E39 # LATIN SMALL LETTER L WITH DOT BELOW AND MACRON
<Multi_key> <underscore> <U1E37>		: "ḹ"	U1E39 # LATIN SMALL LETTER L WITH DOT BELOW AND MACRON
<dead_macron> <dead_belowdot> <l>		: "ḹ"	U1E39 # LATIN SMALL LETTER L WITH DOT BELOW AND MACRON
<dead_macron> <Multi_key> <exclam> <l>		: "ḹ"	U1E39 # LATIN SMALL LETTER L WITH DOT BELOW AND MACRON
<Multi_key> <macron> <dead_belowdot> <l>	: "ḹ"	U1E39 # LATIN SMALL LETTER L WITH DOT BELOW AND MACRON
<Multi_key> <macron> <exclam> <l>		: "ḹ"	U1E39 # LATIN SMALL LETTER L WITH DOT BELOW AND MACRON
<Multi_key> <underscore> <dead_belowdot> <l>	: "ḹ"	U1E39 # LATIN SMALL LETTER L WITH DOT BELOW AND MACRON
<Multi_key> <underscore> <exclam> <l>		: "ḹ"	U1E39 # LATIN SMALL LETTER L WITH DOT BELOW AND MACRON
<dead_belowmacron> <L>				: "Ḻ"	U1E3A # LATIN CAPITAL LETTER L WITH LINE BELOW
<dead_belowmacron> <l>				: "ḻ"	U1E3B # LATIN SMALL LETTER L WITH LINE BELOW
<dead_belowcircumflex> <L>			: "Ḽ"	U1E3C # LATIN CAPITAL LETTER L WITH CIRCUMFLEX BELOW
<dead_belowcircumflex> <l>			: "ḽ"	U1E3D # LATIN SMALL LETTER L WITH CIRCUMFLEX BELOW
<dead_acute> <M>				: "Ḿ"	U1E3E # LATIN CAPITAL LETTER M WITH ACUTE
<Multi_key> <acute> <M>				: "Ḿ"	U1E3E # LATIN CAPITAL LETTER M WITH ACUTE
<Multi_key> <apostrophe> <M>			: "Ḿ"	U1E3E # LATIN CAPITAL LETTER M WITH ACUTE
<dead_acute> <m>				: "ḿ"	U1E3F # LATIN SMALL LETTER M WITH ACUTE
<Multi_key> <acute> <m>				: "ḿ"	U1E3F # LATIN SMALL LETTER M WITH ACUTE
<Multi_key> <apostrophe> <m>			: "ḿ"	U1E3F # LATIN SMALL LETTER M WITH ACUTE
<dead_abovedot> <M>				: "Ṁ"	U1E40 # LATIN CAPITAL LETTER M WITH DOT ABOVE
<Multi_key> <period> <M>			: "Ṁ"	U1E40 # LATIN CAPITAL LETTER M WITH DOT ABOVE
<Multi_key> <M> <period>			: "Ṁ"	U1E40 # LATIN CAPITAL LETTER M WITH DOT ABOVE
<dead_abovedot> <m>				: "ṁ"	U1E41 # LATIN SMALL LETTER M WITH DOT ABOVE
<Multi_key> <period> <m>			: "ṁ"	U1E41 # LATIN SMALL LETTER M WITH DOT ABOVE
<Multi_key> <m> <period>			: "ṁ"	U1E41 # LATIN SMALL LETTER M WITH DOT ABOVE
<dead_belowdot> <M>				: "Ṃ"	U1E42 # LATIN CAPITAL LETTER M WITH DOT BELOW
<Multi_key> <exclam> <M>			: "Ṃ"	U1E42 # LATIN CAPITAL LETTER M WITH DOT BELOW
<dead_belowdot> <m>				: "ṃ"	U1E43 # LATIN SMALL LETTER M WITH DOT BELOW
<Multi_key> <exclam> <m>			: "ṃ"	U1E43 # LATIN SMALL LETTER M WITH DOT BELOW
<dead_abovedot> <N>				: "Ṅ"	U1E44 # LATIN CAPITAL LETTER N WITH DOT ABOVE
<Multi_key> <period> <N>			: "Ṅ"	U1E44 # LATIN CAPITAL LETTER N WITH DOT ABOVE
<dead_abovedot> <n>				: "ṅ"	U1E45 # LATIN SMALL LETTER N WITH DOT ABOVE
<Multi_key> <period> <n>			: "ṅ"	U1E45 # LATIN SMALL LETTER N WITH DOT ABOVE
<dead_belowdot> <N>				: "Ṇ"	U1E46 # LATIN CAPITAL LETTER N WITH DOT BELOW
<Multi_key> <exclam> <N>			: "Ṇ"	U1E46 # LATIN CAPITAL LETTER N WITH DOT BELOW
<dead_belowdot> <n>				: "ṇ"	U1E47 # LATIN SMALL LETTER N WITH DOT BELOW
<Multi_key> <exclam> <n>			: "ṇ"	U1E47 # LATIN SMALL LETTER N WITH DOT BELOW
<dead_belowmacron> <N>				: "Ṉ"	U1E48 # LATIN CAPITAL LETTER N WITH LINE BELOW
<dead_belowmacron> <n>				: "ṉ"	U1E49 # LATIN SMALL LETTER N WITH LINE BELOW
<dead_belowcircumflex> <N>			: "Ṋ"	U1E4A # LATIN CAPITAL LETTER N WITH CIRCUMFLEX BELOW
<dead_belowcircumflex> <n>			: "ṋ"	U1E4B # LATIN SMALL LETTER N WITH CIRCUMFLEX BELOW
<dead_acute> <Otilde>				: "Ṍ"	U1E4C # LATIN CAPITAL LETTER O WITH TILDE AND ACUTE
<Multi_key> <acute> <Otilde>			: "Ṍ"	U1E4C # LATIN CAPITAL LETTER O WITH TILDE AND ACUTE
<Multi_key> <apostrophe> <Otilde>		: "Ṍ"	U1E4C # LATIN CAPITAL LETTER O WITH TILDE AND ACUTE
<dead_acute> <dead_tilde> <O>			: "Ṍ"	U1E4C # LATIN CAPITAL LETTER O WITH TILDE AND ACUTE
<dead_acute> <Multi_key> <asciitilde> <O>	: "Ṍ"	U1E4C # LATIN CAPITAL LETTER O WITH TILDE AND ACUTE
<Multi_key> <acute> <dead_tilde> <O>		: "Ṍ"	U1E4C # LATIN CAPITAL LETTER O WITH TILDE AND ACUTE
<Multi_key> <acute> <asciitilde> <O>		: "Ṍ"	U1E4C # LATIN CAPITAL LETTER O WITH TILDE AND ACUTE
<Multi_key> <apostrophe> <dead_tilde> <O>	: "Ṍ"	U1E4C # LATIN CAPITAL LETTER O WITH TILDE AND ACUTE
<Multi_key> <apostrophe> <asciitilde> <O>	: "Ṍ"	U1E4C # LATIN CAPITAL LETTER O WITH TILDE AND ACUTE
<dead_acute> <otilde>				: "ṍ"	U1E4D # LATIN SMALL LETTER O WITH TILDE AND ACUTE
<Multi_key> <acute> <otilde>			: "ṍ"	U1E4D # LATIN SMALL LETTER O WITH TILDE AND ACUTE
<Multi_key> <apostrophe> <otilde>		: "ṍ"	U1E4D # LATIN SMALL LETTER O WITH TILDE AND ACUTE
<dead_acute> <dead_tilde> <o>			: "ṍ"	U1E4D # LATIN SMALL LETTER O WITH TILDE AND ACUTE
<dead_acute> <Multi_key> <asciitilde> <o>	: "ṍ"	U1E4D # LATIN SMALL LETTER O WITH TILDE AND ACUTE
<Multi_key> <acute> <dead_tilde> <o>		: "ṍ"	U1E4D # LATIN SMALL LETTER O WITH TILDE AND ACUTE
<Multi_key> <acute> <asciitilde> <o>		: "ṍ"	U1E4D # LATIN SMALL LETTER O WITH TILDE AND ACUTE
<Multi_key> <apostrophe> <dead_tilde> <o>	: "ṍ"	U1E4D # LATIN SMALL LETTER O WITH TILDE AND ACUTE
<Multi_key> <apostrophe> <asciitilde> <o>	: "ṍ"	U1E4D # LATIN SMALL LETTER O WITH TILDE AND ACUTE
<dead_diaeresis> <Otilde>			: "Ṏ"	U1E4E # LATIN CAPITAL LETTER O WITH TILDE AND DIAERESIS
<Multi_key> <quotedbl> <Otilde>			: "Ṏ"	U1E4E # LATIN CAPITAL LETTER O WITH TILDE AND DIAERESIS
<dead_diaeresis> <dead_tilde> <O>		: "Ṏ"	U1E4E # LATIN CAPITAL LETTER O WITH TILDE AND DIAERESIS
<dead_diaeresis> <Multi_key> <asciitilde> <O>	: "Ṏ"	U1E4E # LATIN CAPITAL LETTER O WITH TILDE AND DIAERESIS
<Multi_key> <quotedbl> <dead_tilde> <O>		: "Ṏ"	U1E4E # LATIN CAPITAL LETTER O WITH TILDE AND DIAERESIS
<Multi_key> <quotedbl> <asciitilde> <O>		: "Ṏ"	U1E4E # LATIN CAPITAL LETTER O WITH TILDE AND DIAERESIS
<dead_diaeresis> <otilde>			: "ṏ"	U1E4F # LATIN SMALL LETTER O WITH TILDE AND DIAERESIS
<Multi_key> <quotedbl> <otilde>			: "ṏ"	U1E4F # LATIN SMALL LETTER O WITH TILDE AND DIAERESIS
<dead_diaeresis> <dead_tilde> <o>		: "ṏ"	U1E4F # LATIN SMALL LETTER O WITH TILDE AND DIAERESIS
<dead_diaeresis> <Multi_key> <asciitilde> <o>	: "ṏ"	U1E4F # LATIN SMALL LETTER O WITH TILDE AND DIAERESIS
<Multi_key> <quotedbl> <dead_tilde> <o>		: "ṏ"	U1E4F # LATIN SMALL LETTER O WITH TILDE AND DIAERESIS
<Multi_key> <quotedbl> <asciitilde> <o>		: "ṏ"	U1E4F # LATIN SMALL LETTER O WITH TILDE AND DIAERESIS
<dead_grave> <Omacron>				: "Ṑ"	U1E50 # LATIN CAPITAL LETTER O WITH MACRON AND GRAVE
<Multi_key> <grave> <Omacron>			: "Ṑ"	U1E50 # LATIN CAPITAL LETTER O WITH MACRON AND GRAVE
<dead_grave> <dead_macron> <O>			: "Ṑ"	U1E50 # LATIN CAPITAL LETTER O WITH MACRON AND GRAVE
<dead_grave> <Multi_key> <macron> <O>		: "Ṑ"	U1E50 # LATIN CAPITAL LETTER O WITH MACRON AND GRAVE
<dead_grave> <Multi_key> <underscore> <O>	: "Ṑ"	U1E50 # LATIN CAPITAL LETTER O WITH MACRON AND GRAVE
<Multi_key> <grave> <dead_macron> <O>		: "Ṑ"	U1E50 # LATIN CAPITAL LETTER O WITH MACRON AND GRAVE
<Multi_key> <grave> <macron> <O>		: "Ṑ"	U1E50 # LATIN CAPITAL LETTER O WITH MACRON AND GRAVE
<Multi_key> <grave> <underscore> <O>		: "Ṑ"	U1E50 # LATIN CAPITAL LETTER O WITH MACRON AND GRAVE
<dead_grave> <omacron>				: "ṑ"	U1E51 # LATIN SMALL LETTER O WITH MACRON AND GRAVE
<Multi_key> <grave> <omacron>			: "ṑ"	U1E51 # LATIN SMALL LETTER O WITH MACRON AND GRAVE
<dead_grave> <dead_macron> <o>			: "ṑ"	U1E51 # LATIN SMALL LETTER O WITH MACRON AND GRAVE
<dead_grave> <Multi_key> <macron> <o>		: "ṑ"	U1E51 # LATIN SMALL LETTER O WITH MACRON AND GRAVE
<dead_grave> <Multi_key> <underscore> <o>	: "ṑ"	U1E51 # LATIN SMALL LETTER O WITH MACRON AND GRAVE
<Multi_key> <grave> <dead_macron> <o>		: "ṑ"	U1E51 # LATIN SMALL LETTER O WITH MACRON AND GRAVE
<Multi_key> <grave> <macron> <o>		: "ṑ"	U1E51 # LATIN SMALL LETTER O WITH MACRON AND GRAVE
<Multi_key> <grave> <underscore> <o>		: "ṑ"	U1E51 # LATIN SMALL LETTER O WITH MACRON AND GRAVE
<dead_acute> <Omacron>				: "Ṓ"	U1E52 # LATIN CAPITAL LETTER O WITH MACRON AND ACUTE
<Multi_key> <acute> <Omacron>			: "Ṓ"	U1E52 # LATIN CAPITAL LETTER O WITH MACRON AND ACUTE
<Multi_key> <apostrophe> <Omacron>		: "Ṓ"	U1E52 # LATIN CAPITAL LETTER O WITH MACRON AND ACUTE
<dead_acute> <dead_macron> <O>			: "Ṓ"	U1E52 # LATIN CAPITAL LETTER O WITH MACRON AND ACUTE
<dead_acute> <Multi_key> <macron> <O>		: "Ṓ"	U1E52 # LATIN CAPITAL LETTER O WITH MACRON AND ACUTE
<dead_acute> <Multi_key> <underscore> <O>	: "Ṓ"	U1E52 # LATIN CAPITAL LETTER O WITH MACRON AND ACUTE
<Multi_key> <acute> <dead_macron> <O>		: "Ṓ"	U1E52 # LATIN CAPITAL LETTER O WITH MACRON AND ACUTE
<Multi_key> <acute> <macron> <O>		: "Ṓ"	U1E52 # LATIN CAPITAL LETTER O WITH MACRON AND ACUTE
<Multi_key> <acute> <underscore> <O>		: "Ṓ"	U1E52 # LATIN CAPITAL LETTER O WITH MACRON AND ACUTE
<Multi_key> <apostrophe> <dead_macron> <O>	: "Ṓ"	U1E52 # LATIN CAPITAL LETTER O WITH MACRON AND ACUTE
<Multi_key> <apostrophe> <macron> <O>		: "Ṓ"	U1E52 # LATIN CAPITAL LETTER O WITH MACRON AND ACUTE
<Multi_key> <apostrophe> <underscore> <O>	: "Ṓ"	U1E52 # LATIN CAPITAL LETTER O WITH MACRON AND ACUTE
<dead_acute> <omacron>				: "ṓ"	U1E53 # LATIN SMALL LETTER O WITH MACRON AND ACUTE
<Multi_key> <acute> <omacron>			: "ṓ"	U1E53 # LATIN SMALL LETTER O WITH MACRON AND ACUTE
<Multi_key> <apostrophe> <omacron>		: "ṓ"	U1E53 # LATIN SMALL LETTER O WITH MACRON AND ACUTE
<dead_acute> <dead_macron> <o>			: "ṓ"	U1E53 # LATIN SMALL LETTER O WITH MACRON AND ACUTE
<dead_acute> <Multi_key> <macron> <o>		: "ṓ"	U1E53 # LATIN SMALL LETTER O WITH MACRON AND ACUTE
<dead_acute> <Multi_key> <underscore> <o>	: "ṓ"	U1E53 # LATIN SMALL LETTER O WITH MACRON AND ACUTE
<Multi_key> <acute> <dead_macron> <o>		: "ṓ"	U1E53 # LATIN SMALL LETTER O WITH MACRON AND ACUTE
<Multi_key> <acute> <macron> <o>		: "ṓ"	U1E53 # LATIN SMALL LETTER O WITH MACRON AND ACUTE
<Multi_key> <acute> <underscore> <o>		: "ṓ"	U1E53 # LATIN SMALL LETTER O WITH MACRON AND ACUTE
<Multi_key> <apostrophe> <dead_macron> <o>	: "ṓ"	U1E53 # LATIN SMALL LETTER O WITH MACRON AND ACUTE
<Multi_key> <apostrophe> <macron> <o>		: "ṓ"	U1E53 # LATIN SMALL LETTER O WITH MACRON AND ACUTE
<Multi_key> <apostrophe> <underscore> <o>	: "ṓ"	U1E53 # LATIN SMALL LETTER O WITH MACRON AND ACUTE
<dead_acute> <P>				: "Ṕ"	U1E54 # LATIN CAPITAL LETTER P WITH ACUTE
<Multi_key> <acute> <P>				: "Ṕ"	U1E54 # LATIN CAPITAL LETTER P WITH ACUTE
<Multi_key> <apostrophe> <P>			: "Ṕ"	U1E54 # LATIN CAPITAL LETTER P WITH ACUTE
<dead_acute> <p>				: "ṕ"	U1E55 # LATIN SMALL LETTER P WITH ACUTE
<Multi_key> <acute> <p>				: "ṕ"	U1E55 # LATIN SMALL LETTER P WITH ACUTE
<Multi_key> <apostrophe> <p>			: "ṕ"	U1E55 # LATIN SMALL LETTER P WITH ACUTE
<dead_abovedot> <P>				: "Ṗ"	U1E56 # LATIN CAPITAL LETTER P WITH DOT ABOVE
<Multi_key> <period> <P>			: "Ṗ"	U1E56 # LATIN CAPITAL LETTER P WITH DOT ABOVE
<Multi_key> <P> <period>			: "Ṗ"	U1E56 # LATIN CAPITAL LETTER P WITH DOT ABOVE
<dead_abovedot> <p>				: "ṗ"	U1E57 # LATIN SMALL LETTER P WITH DOT ABOVE
<Multi_key> <period> <p>			: "ṗ"	U1E57 # LATIN SMALL LETTER P WITH DOT ABOVE
<Multi_key> <p> <period>			: "ṗ"	U1E57 # LATIN SMALL LETTER P WITH DOT ABOVE
<dead_abovedot> <R>				: "Ṙ"	U1E58 # LATIN CAPITAL LETTER R WITH DOT ABOVE
<Multi_key> <period> <R>			: "Ṙ"	U1E58 # LATIN CAPITAL LETTER R WITH DOT ABOVE
<dead_abovedot> <r>				: "ṙ"	U1E59 # LATIN SMALL LETTER R WITH DOT ABOVE
<Multi_key> <period> <r>			: "ṙ"	U1E59 # LATIN SMALL LETTER R WITH DOT ABOVE
<dead_belowdot> <R>				: "Ṛ"	U1E5A # LATIN CAPITAL LETTER R WITH DOT BELOW
<Multi_key> <exclam> <R>			: "Ṛ"	U1E5A # LATIN CAPITAL LETTER R WITH DOT BELOW
<dead_belowdot> <r>				: "ṛ"	U1E5B # LATIN SMALL LETTER R WITH DOT BELOW
<Multi_key> <exclam> <r>			: "ṛ"	U1E5B # LATIN SMALL LETTER R WITH DOT BELOW
<dead_macron> <U1E5A>				: "Ṝ"	U1E5C # LATIN CAPITAL LETTER R WITH DOT BELOW AND MACRON
<Multi_key> <macron> <U1E5A>			: "Ṝ"	U1E5C # LATIN CAPITAL LETTER R WITH DOT BELOW AND MACRON
<Multi_key> <underscore> <U1E5A>		: "Ṝ"	U1E5C # LATIN CAPITAL LETTER R WITH DOT BELOW AND MACRON
<dead_macron> <dead_belowdot> <R>		: "Ṝ"	U1E5C # LATIN CAPITAL LETTER R WITH DOT BELOW AND MACRON
<dead_macron> <Multi_key> <exclam> <R>		: "Ṝ"	U1E5C # LATIN CAPITAL LETTER R WITH DOT BELOW AND MACRON
<Multi_key> <macron> <dead_belowdot> <R>	: "Ṝ"	U1E5C # LATIN CAPITAL LETTER R WITH DOT BELOW AND MACRON
<Multi_key> <macron> <exclam> <R>		: "Ṝ"	U1E5C # LATIN CAPITAL LETTER R WITH DOT BELOW AND MACRON
<Multi_key> <underscore> <dead_belowdot> <R>	: "Ṝ"	U1E5C # LATIN CAPITAL LETTER R WITH DOT BELOW AND MACRON
<Multi_key> <underscore> <exclam> <R>		: "Ṝ"	U1E5C # LATIN CAPITAL LETTER R WITH DOT BELOW AND MACRON
<dead_macron> <U1E5B>				: "ṝ"	U1E5D # LATIN SMALL LETTER R WITH DOT BELOW AND MACRON
<Multi_key> <macron> <U1E5B>			: "ṝ"	U1E5D # LATIN SMALL LETTER R WITH DOT BELOW AND MACRON
<Multi_key> <underscore> <U1E5B>		: "ṝ"	U1E5D # LATIN SMALL LETTER R WITH DOT BELOW AND MACRON
<dead_macron> <dead_belowdot> <r>		: "ṝ"	U1E5D # LATIN SMALL LETTER R WITH DOT BELOW AND MACRON
<dead_macron> <Multi_key> <exclam> <r>		: "ṝ"	U1E5D # LATIN SMALL LETTER R WITH DOT BELOW AND MACRON
<Multi_key> <macron> <dead_belowdot> <r>	: "ṝ"	U1E5D # LATIN SMALL LETTER R WITH DOT BELOW AND MACRON
<Multi_key> <macron> <exclam> <r>		: "ṝ"	U1E5D # LATIN SMALL LETTER R WITH DOT BELOW AND MACRON
<Multi_key> <underscore> <dead_belowdot> <r>	: "ṝ"	U1E5D # LATIN SMALL LETTER R WITH DOT BELOW AND MACRON
<Multi_key> <underscore> <exclam> <r>		: "ṝ"	U1E5D # LATIN SMALL LETTER R WITH DOT BELOW AND MACRON
<dead_belowmacron> <R>				: "Ṟ"	U1E5E # LATIN CAPITAL LETTER R WITH LINE BELOW
<dead_belowmacron> <r>				: "ṟ"	U1E5F # LATIN SMALL LETTER R WITH LINE BELOW
<dead_abovedot> <S>				: "Ṡ"	U1E60 # LATIN CAPITAL LETTER S WITH DOT ABOVE
<Multi_key> <period> <S>			: "Ṡ"	U1E60 # LATIN CAPITAL LETTER S WITH DOT ABOVE
<Multi_key> <S> <period>			: "Ṡ"	U1E60 # LATIN CAPITAL LETTER S WITH DOT ABOVE
<dead_abovedot> <s>				: "ṡ"	U1E61 # LATIN SMALL LETTER S WITH DOT ABOVE
<Multi_key> <period> <s>			: "ṡ"	U1E61 # LATIN SMALL LETTER S WITH DOT ABOVE
<Multi_key> <s> <period>			: "ṡ"	U1E61 # LATIN SMALL LETTER S WITH DOT ABOVE
<dead_belowdot> <S>				: "Ṣ"	U1E62 # LATIN CAPITAL LETTER S WITH DOT BELOW
<Multi_key> <exclam> <S>			: "Ṣ"	U1E62 # LATIN CAPITAL LETTER S WITH DOT BELOW
<dead_belowdot> <s>				: "ṣ"	U1E63 # LATIN SMALL LETTER S WITH DOT BELOW
<Multi_key> <exclam> <s>			: "ṣ"	U1E63 # LATIN SMALL LETTER S WITH DOT BELOW
<dead_abovedot> <Sacute>			: "Ṥ"	U1E64 # LATIN CAPITAL LETTER S WITH ACUTE AND DOT ABOVE
<Multi_key> <period> <Sacute>			: "Ṥ"	U1E64 # LATIN CAPITAL LETTER S WITH ACUTE AND DOT ABOVE
<dead_abovedot> <dead_acute> <S>		: "Ṥ"	U1E64 # LATIN CAPITAL LETTER S WITH ACUTE AND DOT ABOVE
<dead_abovedot> <Multi_key> <acute> <S>		: "Ṥ"	U1E64 # LATIN CAPITAL LETTER S WITH ACUTE AND DOT ABOVE
<dead_abovedot> <Multi_key> <apostrophe> <S>	: "Ṥ"	U1E64 # LATIN CAPITAL LETTER S WITH ACUTE AND DOT ABOVE
<Multi_key> <period> <dead_acute> <S>		: "Ṥ"	U1E64 # LATIN CAPITAL LETTER S WITH ACUTE AND DOT ABOVE
<Multi_key> <period> <acute> <S>		: "Ṥ"	U1E64 # LATIN CAPITAL LETTER S WITH ACUTE AND DOT ABOVE
<Multi_key> <period> <apostrophe> <S>		: "Ṥ"	U1E64 # LATIN CAPITAL LETTER S WITH ACUTE AND DOT ABOVE
<dead_abovedot> <sacute>			: "ṥ"	U1E65 # LATIN SMALL LETTER S WITH ACUTE AND DOT ABOVE
<Multi_key> <period> <sacute>			: "ṥ"	U1E65 # LATIN SMALL LETTER S WITH ACUTE AND DOT ABOVE
<dead_abovedot> <dead_acute> <s>		: "ṥ"	U1E65 # LATIN SMALL LETTER S WITH ACUTE AND DOT ABOVE
<dead_abovedot> <Multi_key> <acute> <s>		: "ṥ"	U1E65 # LATIN SMALL LETTER S WITH ACUTE AND DOT ABOVE
<dead_abovedot> <Multi_key> <apostrophe> <s>	: "ṥ"	U1E65 # LATIN SMALL LETTER S WITH ACUTE AND DOT ABOVE
<Multi_key> <period> <dead_acute> <s>		: "ṥ"	U1E65 # LATIN SMALL LETTER S WITH ACUTE AND DOT ABOVE
<Multi_key> <period> <acute> <s>		: "ṥ"	U1E65 # LATIN SMALL LETTER S WITH ACUTE AND DOT ABOVE
<Multi_key> <period> <apostrophe> <s>		: "ṥ"	U1E65 # LATIN SMALL LETTER S WITH ACUTE AND DOT ABOVE
<dead_abovedot> <Scaron>			: "Ṧ"	U1E66 # LATIN CAPITAL LETTER S WITH CARON AND DOT ABOVE
<Multi_key> <period> <Scaron>			: "Ṧ"	U1E66 # LATIN CAPITAL LETTER S WITH CARON AND DOT ABOVE
<dead_abovedot> <dead_caron> <S>		: "Ṧ"	U1E66 # LATIN CAPITAL LETTER S WITH CARON AND DOT ABOVE
<dead_abovedot> <Multi_key> <c> <S>		: "Ṧ"	U1E66 # LATIN CAPITAL LETTER S WITH CARON AND DOT ABOVE
<Multi_key> <period> <dead_caron> <S>		: "Ṧ"	U1E66 # LATIN CAPITAL LETTER S WITH CARON AND DOT ABOVE
<dead_abovedot> <scaron>			: "ṧ"	U1E67 # LATIN SMALL LETTER S WITH CARON AND DOT ABOVE
<Multi_key> <period> <scaron>			: "ṧ"	U1E67 # LATIN SMALL LETTER S WITH CARON AND DOT ABOVE
<dead_abovedot> <dead_caron> <s>		: "ṧ"	U1E67 # LATIN SMALL LETTER S WITH CARON AND DOT ABOVE
<dead_abovedot> <Multi_key> <c> <s>		: "ṧ"	U1E67 # LATIN SMALL LETTER S WITH CARON AND DOT ABOVE
<Multi_key> <period> <dead_caron> <s>		: "ṧ"	U1E67 # LATIN SMALL LETTER S WITH CARON AND DOT ABOVE
<dead_abovedot> <U1E62>				: "Ṩ"	U1E68 # LATIN CAPITAL LETTER S WITH DOT BELOW AND DOT ABOVE
<Multi_key> <period> <U1E62>			: "Ṩ"	U1E68 # LATIN CAPITAL LETTER S WITH DOT BELOW AND DOT ABOVE
<dead_abovedot> <dead_belowdot> <S>		: "Ṩ"	U1E68 # LATIN CAPITAL LETTER S WITH DOT BELOW AND DOT ABOVE
<dead_abovedot> <Multi_key> <exclam> <S>	: "Ṩ"	U1E68 # LATIN CAPITAL LETTER S WITH DOT BELOW AND DOT ABOVE
<Multi_key> <period> <dead_belowdot> <S>	: "Ṩ"	U1E68 # LATIN CAPITAL LETTER S WITH DOT BELOW AND DOT ABOVE
<Multi_key> <period> <exclam> <S>		: "Ṩ"	U1E68 # LATIN CAPITAL LETTER S WITH DOT BELOW AND DOT ABOVE
<dead_abovedot> <U1E63>				: "ṩ"	U1E69 # LATIN SMALL LETTER S WITH DOT BELOW AND DOT ABOVE
<Multi_key> <period> <U1E63>			: "ṩ"	U1E69 # LATIN SMALL LETTER S WITH DOT BELOW AND DOT ABOVE
<dead_abovedot> <dead_belowdot> <s>		: "ṩ"	U1E69 # LATIN SMALL LETTER S WITH DOT BELOW AND DOT ABOVE
<dead_abovedot> <Multi_key> <exclam> <s>	: "ṩ"	U1E69 # LATIN SMALL LETTER S WITH DOT BELOW AND DOT ABOVE
<Multi_key> <period> <dead_belowdot> <s>	: "ṩ"	U1E69 # LATIN SMALL LETTER S WITH DOT BELOW AND DOT ABOVE
<Multi_key> <period> <exclam> <s>		: "ṩ"	U1E69 # LATIN SMALL LETTER S WITH DOT BELOW AND DOT ABOVE
<dead_abovedot> <T>				: "Ṫ"	U1E6A # LATIN CAPITAL LETTER T WITH DOT ABOVE
<Multi_key> <period> <T>			: "Ṫ"	U1E6A # LATIN CAPITAL LETTER T WITH DOT ABOVE
<Multi_key> <T> <period>			: "Ṫ"	U1E6A # LATIN CAPITAL LETTER T WITH DOT ABOVE
<dead_abovedot> <t>				: "ṫ"	U1E6B # LATIN SMALL LETTER T WITH DOT ABOVE
<Multi_key> <period> <t>			: "ṫ"	U1E6B # LATIN SMALL LETTER T WITH DOT ABOVE
<Multi_key> <t> <period>			: "ṫ"	U1E6B # LATIN SMALL LETTER T WITH DOT ABOVE
<dead_belowdot> <T>				: "Ṭ"	U1E6C # LATIN CAPITAL LETTER T WITH DOT BELOW
<Multi_key> <exclam> <T>			: "Ṭ"	U1E6C # LATIN CAPITAL LETTER T WITH DOT BELOW
<dead_belowdot> <t>				: "ṭ"	U1E6D # LATIN SMALL LETTER T WITH DOT BELOW
<Multi_key> <exclam> <t>			: "ṭ"	U1E6D # LATIN SMALL LETTER T WITH DOT BELOW
<dead_belowmacron> <T>				: "Ṯ"	U1E6E # LATIN CAPITAL LETTER T WITH LINE BELOW
<dead_belowmacron> <t>				: "ṯ"	U1E6F # LATIN SMALL LETTER T WITH LINE BELOW
<dead_belowcircumflex> <T>			: "Ṱ"	U1E70 # LATIN CAPITAL LETTER T WITH CIRCUMFLEX BELOW
<dead_belowcircumflex> <t>			: "ṱ"	U1E71 # LATIN SMALL LETTER T WITH CIRCUMFLEX BELOW
<dead_belowdiaeresis> <U>			: "Ṳ"	U1E72 # LATIN CAPITAL LETTER U WITH DIAERESIS BELOW
<dead_belowdiaeresis> <u>			: "ṳ"	U1E73 # LATIN SMALL LETTER U WITH DIAERESIS BELOW
<dead_belowtilde> <U>				: "Ṵ"	U1E74 # LATIN CAPITAL LETTER U WITH TILDE BELOW
<dead_belowtilde> <u>				: "ṵ"	U1E75 # LATIN SMALL LETTER U WITH TILDE BELOW
<dead_belowcircumflex> <U>			: "Ṷ"	U1E76 # LATIN CAPITAL LETTER U WITH CIRCUMFLEX BELOW
<dead_belowcircumflex> <u>			: "ṷ"	U1E77 # LATIN SMALL LETTER U WITH CIRCUMFLEX BELOW
<dead_acute> <Utilde>				: "Ṹ"	U1E78 # LATIN CAPITAL LETTER U WITH TILDE AND ACUTE
<Multi_key> <acute> <Utilde>			: "Ṹ"	U1E78 # LATIN CAPITAL LETTER U WITH TILDE AND ACUTE
<Multi_key> <apostrophe> <Utilde>		: "Ṹ"	U1E78 # LATIN CAPITAL LETTER U WITH TILDE AND ACUTE
<dead_acute> <dead_tilde> <U>			: "Ṹ"	U1E78 # LATIN CAPITAL LETTER U WITH TILDE AND ACUTE
<dead_acute> <Multi_key> <asciitilde> <U>	: "Ṹ"	U1E78 # LATIN CAPITAL LETTER U WITH TILDE AND ACUTE
<Multi_key> <acute> <dead_tilde> <U>		: "Ṹ"	U1E78 # LATIN CAPITAL LETTER U WITH TILDE AND ACUTE
<Multi_key> <acute> <asciitilde> <U>		: "Ṹ"	U1E78 # LATIN CAPITAL LETTER U WITH TILDE AND ACUTE
<Multi_key> <apostrophe> <dead_tilde> <U>	: "Ṹ"	U1E78 # LATIN CAPITAL LETTER U WITH TILDE AND ACUTE
<Multi_key> <apostrophe> <asciitilde> <U>	: "Ṹ"	U1E78 # LATIN CAPITAL LETTER U WITH TILDE AND ACUTE
<dead_acute> <utilde>				: "ṹ"	U1E79 # LATIN SMALL LETTER U WITH TILDE AND ACUTE
<Multi_key> <acute> <utilde>			: "ṹ"	U1E79 # LATIN SMALL LETTER U WITH TILDE AND ACUTE
<Multi_key> <apostrophe> <utilde>		: "ṹ"	U1E79 # LATIN SMALL LETTER U WITH TILDE AND ACUTE
<dead_acute> <dead_tilde> <u>			: "ṹ"	U1E79 # LATIN SMALL LETTER U WITH TILDE AND ACUTE
<dead_acute> <Multi_key> <asciitilde> <u>	: "ṹ"	U1E79 # LATIN SMALL LETTER U WITH TILDE AND ACUTE
<Multi_key> <acute> <dead_tilde> <u>		: "ṹ"	U1E79 # LATIN SMALL LETTER U WITH TILDE AND ACUTE
<Multi_key> <acute> <asciitilde> <u>		: "ṹ"	U1E79 # LATIN SMALL LETTER U WITH TILDE AND ACUTE
<Multi_key> <apostrophe> <dead_tilde> <u>	: "ṹ"	U1E79 # LATIN SMALL LETTER U WITH TILDE AND ACUTE
<Multi_key> <apostrophe> <asciitilde> <u>	: "ṹ"	U1E79 # LATIN SMALL LETTER U WITH TILDE AND ACUTE
<dead_diaeresis> <Umacron>			: "Ṻ"	U1E7A # LATIN CAPITAL LETTER U WITH MACRON AND DIAERESIS
<Multi_key> <quotedbl> <Umacron>		: "Ṻ"	U1E7A # LATIN CAPITAL LETTER U WITH MACRON AND DIAERESIS
<dead_diaeresis> <dead_macron> <U>		: "Ṻ"	U1E7A # LATIN CAPITAL LETTER U WITH MACRON AND DIAERESIS
<dead_diaeresis> <Multi_key> <macron> <U>	: "Ṻ"	U1E7A # LATIN CAPITAL LETTER U WITH MACRON AND DIAERESIS
<dead_diaeresis> <Multi_key> <underscore> <U>	: "Ṻ"	U1E7A # LATIN CAPITAL LETTER U WITH MACRON AND DIAERESIS
<Multi_key> <quotedbl> <dead_macron> <U>	: "Ṻ"	U1E7A # LATIN CAPITAL LETTER U WITH MACRON AND DIAERESIS
<Multi_key> <quotedbl> <macron> <U>		: "Ṻ"	U1E7A # LATIN CAPITAL LETTER U WITH MACRON AND DIAERESIS
<Multi_key> <quotedbl> <underscore> <U>		: "Ṻ"	U1E7A # LATIN CAPITAL LETTER U WITH MACRON AND DIAERESIS
<dead_diaeresis> <umacron>			: "ṻ"	U1E7B # LATIN SMALL LETTER U WITH MACRON AND DIAERESIS
<Multi_key> <quotedbl> <umacron>		: "ṻ"	U1E7B # LATIN SMALL LETTER U WITH MACRON AND DIAERESIS
<dead_diaeresis> <dead_macron> <u>		: "ṻ"	U1E7B # LATIN SMALL LETTER U WITH MACRON AND DIAERESIS
<dead_diaeresis> <Multi_key> <macron> <u>	: "ṻ"	U1E7B # LATIN SMALL LETTER U WITH MACRON AND DIAERESIS
<dead_diaeresis> <Multi_key> <underscore> <u>	: "ṻ"	U1E7B # LATIN SMALL LETTER U WITH MACRON AND DIAERESIS
<Multi_key> <quotedbl> <dead_macron> <u>	: "ṻ"	U1E7B # LATIN SMALL LETTER U WITH MACRON AND DIAERESIS
<Multi_key> <quotedbl> <macron> <u>		: "ṻ"	U1E7B # LATIN SMALL LETTER U WITH MACRON AND DIAERESIS
<Multi_key> <quotedbl> <underscore> <u>		: "ṻ"	U1E7B # LATIN SMALL LETTER U WITH MACRON AND DIAERESIS
<dead_tilde> <V>				: "Ṽ"	U1E7C # LATIN CAPITAL LETTER V WITH TILDE
<Multi_key> <asciitilde> <V>			: "Ṽ"	U1E7C # LATIN CAPITAL LETTER V WITH TILDE
<dead_tilde> <v>				: "ṽ"	U1E7D # LATIN SMALL LETTER V WITH TILDE
<Multi_key> <asciitilde> <v>			: "ṽ"	U1E7D # LATIN SMALL LETTER V WITH TILDE
<dead_belowdot> <V>				: "Ṿ"	U1E7E # LATIN CAPITAL LETTER V WITH DOT BELOW
<Multi_key> <exclam> <V>			: "Ṿ"	U1E7E # LATIN CAPITAL LETTER V WITH DOT BELOW
<dead_belowdot> <v>				: "ṿ"	U1E7F # LATIN SMALL LETTER V WITH DOT BELOW
<Multi_key> <exclam> <v>			: "ṿ"	U1E7F # LATIN SMALL LETTER V WITH DOT BELOW
<dead_grave> <W>				: "Ẁ"	U1E80 # LATIN CAPITAL LETTER W WITH GRAVE
<Multi_key> <grave> <W>				: "Ẁ"	U1E80 # LATIN CAPITAL LETTER W WITH GRAVE
<dead_grave> <w>				: "ẁ"	U1E81 # LATIN SMALL LETTER W WITH GRAVE
<Multi_key> <grave> <w>				: "ẁ"	U1E81 # LATIN SMALL LETTER W WITH GRAVE
<dead_acute> <W>				: "Ẃ"	U1E82 # LATIN CAPITAL LETTER W WITH ACUTE
<Multi_key> <acute> <W>				: "Ẃ"	U1E82 # LATIN CAPITAL LETTER W WITH ACUTE
<Multi_key> <apostrophe> <W>			: "Ẃ"	U1E82 # LATIN CAPITAL LETTER W WITH ACUTE
<dead_acute> <w>				: "ẃ"	U1E83 # LATIN SMALL LETTER W WITH ACUTE
<Multi_key> <acute> <w>				: "ẃ"	U1E83 # LATIN SMALL LETTER W WITH ACUTE
<Multi_key> <apostrophe> <w>			: "ẃ"	U1E83 # LATIN SMALL LETTER W WITH ACUTE
<dead_diaeresis> <W>				: "Ẅ"	U1E84 # LATIN CAPITAL LETTER W WITH DIAERESIS
<Multi_key> <quotedbl> <W>			: "Ẅ"	U1E84 # LATIN CAPITAL LETTER W WITH DIAERESIS
<dead_diaeresis> <w>				: "ẅ"	U1E85 # LATIN SMALL LETTER W WITH DIAERESIS
<Multi_key> <quotedbl> <w>			: "ẅ"	U1E85 # LATIN SMALL LETTER W WITH DIAERESIS
<dead_abovedot> <W>				: "Ẇ"	U1E86 # LATIN CAPITAL LETTER W WITH DOT ABOVE
<Multi_key> <period> <W>			: "Ẇ"	U1E86 # LATIN CAPITAL LETTER W WITH DOT ABOVE
<dead_abovedot> <w>				: "ẇ"	U1E87 # LATIN SMALL LETTER W WITH DOT ABOVE
<Multi_key> <period> <w>			: "ẇ"	U1E87 # LATIN SMALL LETTER W WITH DOT ABOVE
<dead_belowdot> <W>				: "Ẉ"	U1E88 # LATIN CAPITAL LETTER W WITH DOT BELOW
<Multi_key> <exclam> <W>			: "Ẉ"	U1E88 # LATIN CAPITAL LETTER W WITH DOT BELOW
<dead_belowdot> <w>				: "ẉ"	U1E89 # LATIN SMALL LETTER W WITH DOT BELOW
<Multi_key> <exclam> <w>			: "ẉ"	U1E89 # LATIN SMALL LETTER W WITH DOT BELOW
<dead_abovedot> <X>				: "Ẋ"	U1E8A # LATIN CAPITAL LETTER X WITH DOT ABOVE
<Multi_key> <period> <X>			: "Ẋ"	U1E8A # LATIN CAPITAL LETTER X WITH DOT ABOVE
<dead_abovedot> <x>				: "ẋ"	U1E8B # LATIN SMALL LETTER X WITH DOT ABOVE
<Multi_key> <period> <x>			: "ẋ"	U1E8B # LATIN SMALL LETTER X WITH DOT ABOVE
<dead_diaeresis> <X>				: "Ẍ"	U1E8C # LATIN CAPITAL LETTER X WITH DIAERESIS
<Multi_key> <quotedbl> <X>			: "Ẍ"	U1E8C # LATIN CAPITAL LETTER X WITH DIAERESIS
<dead_diaeresis> <x>				: "ẍ"	U1E8D # LATIN SMALL LETTER X WITH DIAERESIS
<Multi_key> <quotedbl> <x>			: "ẍ"	U1E8D # LATIN SMALL LETTER X WITH DIAERESIS
<dead_abovedot> <Y>				: "Ẏ"	U1E8E # LATIN CAPITAL LETTER Y WITH DOT ABOVE
<Multi_key> <period> <Y>			: "Ẏ"	U1E8E # LATIN CAPITAL LETTER Y WITH DOT ABOVE
<dead_abovedot> <y>				: "ẏ"	U1E8F # LATIN SMALL LETTER Y WITH DOT ABOVE
<Multi_key> <period> <y>			: "ẏ"	U1E8F # LATIN SMALL LETTER Y WITH DOT ABOVE
<dead_circumflex> <Z>				: "Ẑ"	U1E90 # LATIN CAPITAL LETTER Z WITH CIRCUMFLEX
<Multi_key> <asciicircum> <Z>			: "Ẑ"	U1E90 # LATIN CAPITAL LETTER Z WITH CIRCUMFLEX
<dead_circumflex> <z>				: "ẑ"	U1E91 # LATIN SMALL LETTER Z WITH CIRCUMFLEX
<Multi_key> <asciicircum> <z>			: "ẑ"	U1E91 # LATIN SMALL LETTER Z WITH CIRCUMFLEX
<dead_belowdot> <Z>				: "Ẓ"	U1E92 # LATIN CAPITAL LETTER Z WITH DOT BELOW
<Multi_key> <exclam> <Z>			: "Ẓ"	U1E92 # LATIN CAPITAL LETTER Z WITH DOT BELOW
<dead_belowdot> <z>				: "ẓ"	U1E93 # LATIN SMALL LETTER Z WITH DOT BELOW
<Multi_key> <exclam> <z>			: "ẓ"	U1E93 # LATIN SMALL LETTER Z WITH DOT BELOW
<dead_belowmacron> <Z>				: "Ẕ"	U1E94 # LATIN CAPITAL LETTER Z WITH LINE BELOW
<dead_belowmacron> <z>				: "ẕ"	U1E95 # LATIN SMALL LETTER Z WITH LINE BELOW
<dead_belowmacron> <h>				: "ẖ"	U1E96 # LATIN SMALL LETTER H WITH LINE BELOW
<dead_diaeresis> <t>				: "ẗ"	U1E97 # LATIN SMALL LETTER T WITH DIAERESIS
<Multi_key> <quotedbl> <t>			: "ẗ"	U1E97 # LATIN SMALL LETTER T WITH DIAERESIS
<dead_abovering> <w>				: "ẘ"	U1E98 # LATIN SMALL LETTER W WITH RING ABOVE
<Multi_key> <o> <w>				: "ẘ"	U1E98 # LATIN SMALL LETTER W WITH RING ABOVE
<dead_abovering> <y>				: "ẙ"	U1E99 # LATIN SMALL LETTER Y WITH RING ABOVE
<Multi_key> <o> <y>				: "ẙ"	U1E99 # LATIN SMALL LETTER Y WITH RING ABOVE
<dead_abovedot> <U017F>				: "ẛ"	U1E9B # LATIN SMALL LETTER LONG S WITH DOT ABOVE
<Multi_key> <period> <U017F>			: "ẛ"	U1E9B # LATIN SMALL LETTER LONG S WITH DOT ABOVE
<dead_abovedot> <Multi_key> <f> <s>		: "ẛ"	U1E9B # LATIN SMALL LETTER LONG S WITH DOT ABOVE
<Multi_key> <dead_abovedot> <f> <s>		: "ẛ"	U1E9B # LATIN SMALL LETTER LONG S WITH DOT ABOVE
<dead_belowdot> <A>				: "Ạ"	U1EA0 # LATIN CAPITAL LETTER A WITH DOT BELOW
<Multi_key> <exclam> <A>			: "Ạ"	U1EA0 # LATIN CAPITAL LETTER A WITH DOT BELOW
<dead_belowdot> <a>				: "ạ"	U1EA1 # LATIN SMALL LETTER A WITH DOT BELOW
<Multi_key> <exclam> <a>			: "ạ"	U1EA1 # LATIN SMALL LETTER A WITH DOT BELOW
<dead_hook> <A>					: "Ả"	U1EA2 # LATIN CAPITAL LETTER A WITH HOOK ABOVE
<Multi_key> <question> <A>			: "Ả"	U1EA2 # LATIN CAPITAL LETTER A WITH HOOK ABOVE
<dead_hook> <a>					: "ả"	U1EA3 # LATIN SMALL LETTER A WITH HOOK ABOVE
<Multi_key> <question> <a>			: "ả"	U1EA3 # LATIN SMALL LETTER A WITH HOOK ABOVE
<dead_acute> <Acircumflex>			: "Ấ"	U1EA4 # LATIN CAPITAL LETTER A WITH CIRCUMFLEX AND ACUTE
<Multi_key> <acute> <Acircumflex>		: "Ấ"	U1EA4 # LATIN CAPITAL LETTER A WITH CIRCUMFLEX AND ACUTE
<Multi_key> <apostrophe> <Acircumflex>		: "Ấ"	U1EA4 # LATIN CAPITAL LETTER A WITH CIRCUMFLEX AND ACUTE
<dead_acute> <dead_circumflex> <A>		: "Ấ"	U1EA4 # LATIN CAPITAL LETTER A WITH CIRCUMFLEX AND ACUTE
<dead_acute> <Multi_key> <asciicircum> <A>	: "Ấ"	U1EA4 # LATIN CAPITAL LETTER A WITH CIRCUMFLEX AND ACUTE
<Multi_key> <acute> <dead_circumflex> <A>	: "Ấ"	U1EA4 # LATIN CAPITAL LETTER A WITH CIRCUMFLEX AND ACUTE
<Multi_key> <acute> <asciicircum> <A>		: "Ấ"	U1EA4 # LATIN CAPITAL LETTER A WITH CIRCUMFLEX AND ACUTE
<Multi_key> <apostrophe> <dead_circumflex> <A>	: "Ấ"	U1EA4 # LATIN CAPITAL LETTER A WITH CIRCUMFLEX AND ACUTE
<Multi_key> <apostrophe> <asciicircum> <A>	: "Ấ"	U1EA4 # LATIN CAPITAL LETTER A WITH CIRCUMFLEX AND ACUTE
<dead_acute> <acircumflex>			: "ấ"	U1EA5 # LATIN SMALL LETTER A WITH CIRCUMFLEX AND ACUTE
<Multi_key> <acute> <acircumflex>		: "ấ"	U1EA5 # LATIN SMALL LETTER A WITH CIRCUMFLEX AND ACUTE
<Multi_key> <apostrophe> <acircumflex>		: "ấ"	U1EA5 # LATIN SMALL LETTER A WITH CIRCUMFLEX AND ACUTE
<dead_acute> <dead_circumflex> <a>		: "ấ"	U1EA5 # LATIN SMALL LETTER A WITH CIRCUMFLEX AND ACUTE
<dead_acute> <Multi_key> <asciicircum> <a>	: "ấ"	U1EA5 # LATIN SMALL LETTER A WITH CIRCUMFLEX AND ACUTE
<Multi_key> <acute> <dead_circumflex> <a>	: "ấ"	U1EA5 # LATIN SMALL LETTER A WITH CIRCUMFLEX AND ACUTE
<Multi_key> <acute> <asciicircum> <a>		: "ấ"	U1EA5 # LATIN SMALL LETTER A WITH CIRCUMFLEX AND ACUTE
<Multi_key> <apostrophe> <dead_circumflex> <a>	: "ấ"	U1EA5 # LATIN SMALL LETTER A WITH CIRCUMFLEX AND ACUTE
<Multi_key> <apostrophe> <asciicircum> <a>	: "ấ"	U1EA5 # LATIN SMALL LETTER A WITH CIRCUMFLEX AND ACUTE
<dead_grave> <Acircumflex>			: "Ầ"	U1EA6 # LATIN CAPITAL LETTER A WITH CIRCUMFLEX AND GRAVE
<Multi_key> <grave> <Acircumflex>		: "Ầ"	U1EA6 # LATIN CAPITAL LETTER A WITH CIRCUMFLEX AND GRAVE
<dead_grave> <dead_circumflex> <A>		: "Ầ"	U1EA6 # LATIN CAPITAL LETTER A WITH CIRCUMFLEX AND GRAVE
<dead_grave> <Multi_key> <asciicircum> <A>	: "Ầ"	U1EA6 # LATIN CAPITAL LETTER A WITH CIRCUMFLEX AND GRAVE
<Multi_key> <grave> <dead_circumflex> <A>	: "Ầ"	U1EA6 # LATIN CAPITAL LETTER A WITH CIRCUMFLEX AND GRAVE
<Multi_key> <grave> <asciicircum> <A>		: "Ầ"	U1EA6 # LATIN CAPITAL LETTER A WITH CIRCUMFLEX AND GRAVE
<dead_grave> <acircumflex>			: "ầ"	U1EA7 # LATIN SMALL LETTER A WITH CIRCUMFLEX AND GRAVE
<Multi_key> <grave> <acircumflex>		: "ầ"	U1EA7 # LATIN SMALL LETTER A WITH CIRCUMFLEX AND GRAVE
<dead_grave> <dead_circumflex> <a>		: "ầ"	U1EA7 # LATIN SMALL LETTER A WITH CIRCUMFLEX AND GRAVE
<dead_grave> <Multi_key> <asciicircum> <a>	: "ầ"	U1EA7 # LATIN SMALL LETTER A WITH CIRCUMFLEX AND GRAVE
<Multi_key> <grave> <dead_circumflex> <a>	: "ầ"	U1EA7 # LATIN SMALL LETTER A WITH CIRCUMFLEX AND GRAVE
<Multi_key> <grave> <asciicircum> <a>		: "ầ"	U1EA7 # LATIN SMALL LETTER A WITH CIRCUMFLEX AND GRAVE
<dead_hook> <Acircumflex>			: "Ẩ"	U1EA8 # LATIN CAPITAL LETTER A WITH CIRCUMFLEX AND HOOK ABOVE
<Multi_key> <question> <Acircumflex>		: "Ẩ"	U1EA8 # LATIN CAPITAL LETTER A WITH CIRCUMFLEX AND HOOK ABOVE
<dead_hook> <dead_circumflex> <A>		: "Ẩ"	U1EA8 # LATIN CAPITAL LETTER A WITH CIRCUMFLEX AND HOOK ABOVE
<dead_hook> <Multi_key> <asciicircum> <A>	: "Ẩ"	U1EA8 # LATIN CAPITAL LETTER A WITH CIRCUMFLEX AND HOOK ABOVE
<Multi_key> <question> <dead_circumflex> <A>	: "Ẩ"	U1EA8 # LATIN CAPITAL LETTER A WITH CIRCUMFLEX AND HOOK ABOVE
<Multi_key> <question> <asciicircum> <A>	: "Ẩ"	U1EA8 # LATIN CAPITAL LETTER A WITH CIRCUMFLEX AND HOOK ABOVE
<dead_hook> <acircumflex>			: "ẩ"	U1EA9 # LATIN SMALL LETTER A WITH CIRCUMFLEX AND HOOK ABOVE
<Multi_key> <question> <acircumflex>		: "ẩ"	U1EA9 # LATIN SMALL LETTER A WITH CIRCUMFLEX AND HOOK ABOVE
<dead_hook> <dead_circumflex> <a>		: "ẩ"	U1EA9 # LATIN SMALL LETTER A WITH CIRCUMFLEX AND HOOK ABOVE
<dead_hook> <Multi_key> <asciicircum> <a>	: "ẩ"	U1EA9 # LATIN SMALL LETTER A WITH CIRCUMFLEX AND HOOK ABOVE
<Multi_key> <question> <dead_circumflex> <a>	: "ẩ"	U1EA9 # LATIN SMALL LETTER A WITH CIRCUMFLEX AND HOOK ABOVE
<Multi_key> <question> <asciicircum> <a>	: "ẩ"	U1EA9 # LATIN SMALL LETTER A WITH CIRCUMFLEX AND HOOK ABOVE
<dead_tilde> <Acircumflex>			: "Ẫ"	U1EAA # LATIN CAPITAL LETTER A WITH CIRCUMFLEX AND TILDE
<Multi_key> <asciitilde> <Acircumflex>		: "Ẫ"	U1EAA # LATIN CAPITAL LETTER A WITH CIRCUMFLEX AND TILDE
<dead_tilde> <dead_circumflex> <A>		: "Ẫ"	U1EAA # LATIN CAPITAL LETTER A WITH CIRCUMFLEX AND TILDE
<dead_tilde> <Multi_key> <asciicircum> <A>	: "Ẫ"	U1EAA # LATIN CAPITAL LETTER A WITH CIRCUMFLEX AND TILDE
<Multi_key> <asciitilde> <dead_circumflex> <A>	: "Ẫ"	U1EAA # LATIN CAPITAL LETTER A WITH CIRCUMFLEX AND TILDE
<Multi_key> <asciitilde> <asciicircum> <A>	: "Ẫ"	U1EAA # LATIN CAPITAL LETTER A WITH CIRCUMFLEX AND TILDE
<dead_tilde> <acircumflex>			: "ẫ"	U1EAB # LATIN SMALL LETTER A WITH CIRCUMFLEX AND TILDE
<Multi_key> <asciitilde> <acircumflex>		: "ẫ"	U1EAB # LATIN SMALL LETTER A WITH CIRCUMFLEX AND TILDE
<dead_tilde> <dead_circumflex> <a>		: "ẫ"	U1EAB # LATIN SMALL LETTER A WITH CIRCUMFLEX AND TILDE
<dead_tilde> <Multi_key> <asciicircum> <a>	: "ẫ"	U1EAB # LATIN SMALL LETTER A WITH CIRCUMFLEX AND TILDE
<Multi_key> <asciitilde> <dead_circumflex> <a>	: "ẫ"	U1EAB # LATIN SMALL LETTER A WITH CIRCUMFLEX AND TILDE
<Multi_key> <asciitilde> <asciicircum> <a>	: "ẫ"	U1EAB # LATIN SMALL LETTER A WITH CIRCUMFLEX AND TILDE
<dead_circumflex> <dead_belowdot> <A>		: "Ậ"	U1EAC # LATIN CAPITAL LETTER A WITH CIRCUMFLEX AND DOT BELOW
<dead_circumflex> <Multi_key> <exclam> <A>	: "Ậ"	U1EAC # LATIN CAPITAL LETTER A WITH CIRCUMFLEX AND DOT BELOW
<Multi_key> <asciicircum> <dead_belowdot> <A>	: "Ậ"	U1EAC # LATIN CAPITAL LETTER A WITH CIRCUMFLEX AND DOT BELOW
<Multi_key> <asciicircum> <exclam> <A>		: "Ậ"	U1EAC # LATIN CAPITAL LETTER A WITH CIRCUMFLEX AND DOT BELOW
<dead_belowdot> <Acircumflex>			: "Ậ"	U1EAC # LATIN CAPITAL LETTER A WITH CIRCUMFLEX AND DOT BELOW
<dead_circumflex> <dead_belowdot> <a>		: "ậ"	U1EAD # LATIN SMALL LETTER A WITH CIRCUMFLEX AND DOT BELOW
<dead_circumflex> <Multi_key> <exclam> <a>	: "ậ"	U1EAD # LATIN SMALL LETTER A WITH CIRCUMFLEX AND DOT BELOW
<Multi_key> <asciicircum> <dead_belowdot> <a>	: "ậ"	U1EAD # LATIN SMALL LETTER A WITH CIRCUMFLEX AND DOT BELOW
<Multi_key> <asciicircum> <exclam> <a>		: "ậ"	U1EAD # LATIN SMALL LETTER A WITH CIRCUMFLEX AND DOT BELOW
<dead_belowdot> <acircumflex>			: "ậ"	U1EAD # LATIN SMALL LETTER A WITH CIRCUMFLEX AND DOT BELOW
<dead_acute> <Abreve>				: "Ắ"	U1EAE # LATIN CAPITAL LETTER A WITH BREVE AND ACUTE
<Multi_key> <acute> <Abreve>			: "Ắ"	U1EAE # LATIN CAPITAL LETTER A WITH BREVE AND ACUTE
<Multi_key> <apostrophe> <Abreve>		: "Ắ"	U1EAE # LATIN CAPITAL LETTER A WITH BREVE AND ACUTE
<dead_acute> <dead_breve> <A>			: "Ắ"	U1EAE # LATIN CAPITAL LETTER A WITH BREVE AND ACUTE
<dead_acute> <Multi_key> <U> <A>		: "Ắ"	U1EAE # LATIN CAPITAL LETTER A WITH BREVE AND ACUTE
<dead_acute> <Multi_key> <b> <A>		: "Ắ"	U1EAE # LATIN CAPITAL LETTER A WITH BREVE AND ACUTE
<Multi_key> <acute> <dead_breve> <A>		: "Ắ"	U1EAE # LATIN CAPITAL LETTER A WITH BREVE AND ACUTE
<Multi_key> <acute> <b> <A>			: "Ắ"	U1EAE # LATIN CAPITAL LETTER A WITH BREVE AND ACUTE
<Multi_key> <apostrophe> <dead_breve> <A>	: "Ắ"	U1EAE # LATIN CAPITAL LETTER A WITH BREVE AND ACUTE
<Multi_key> <apostrophe> <b> <A>		: "Ắ"	U1EAE # LATIN CAPITAL LETTER A WITH BREVE AND ACUTE
<dead_acute> <abreve>				: "ắ"	U1EAF # LATIN SMALL LETTER A WITH BREVE AND ACUTE
<Multi_key> <acute> <abreve>			: "ắ"	U1EAF # LATIN SMALL LETTER A WITH BREVE AND ACUTE
<Multi_key> <apostrophe> <abreve>		: "ắ"	U1EAF # LATIN SMALL LETTER A WITH BREVE AND ACUTE
<dead_acute> <dead_breve> <a>			: "ắ"	U1EAF # LATIN SMALL LETTER A WITH BREVE AND ACUTE
<dead_acute> <Multi_key> <U> <a>		: "ắ"	U1EAF # LATIN SMALL LETTER A WITH BREVE AND ACUTE
<dead_acute> <Multi_key> <b> <a>		: "ắ"	U1EAF # LATIN SMALL LETTER A WITH BREVE AND ACUTE
<Multi_key> <acute> <dead_breve> <a>		: "ắ"	U1EAF # LATIN SMALL LETTER A WITH BREVE AND ACUTE
<Multi_key> <acute> <b> <a>			: "ắ"	U1EAF # LATIN SMALL LETTER A WITH BREVE AND ACUTE
<Multi_key> <apostrophe> <dead_breve> <a>	: "ắ"	U1EAF # LATIN SMALL LETTER A WITH BREVE AND ACUTE
<Multi_key> <apostrophe> <b> <a>		: "ắ"	U1EAF # LATIN SMALL LETTER A WITH BREVE AND ACUTE
<dead_grave> <Abreve>				: "Ằ"	U1EB0 # LATIN CAPITAL LETTER A WITH BREVE AND GRAVE
<Multi_key> <grave> <Abreve>			: "Ằ"	U1EB0 # LATIN CAPITAL LETTER A WITH BREVE AND GRAVE
<dead_grave> <dead_breve> <A>			: "Ằ"	U1EB0 # LATIN CAPITAL LETTER A WITH BREVE AND GRAVE
<dead_grave> <Multi_key> <U> <A>		: "Ằ"	U1EB0 # LATIN CAPITAL LETTER A WITH BREVE AND GRAVE
<dead_grave> <Multi_key> <b> <A>		: "Ằ"	U1EB0 # LATIN CAPITAL LETTER A WITH BREVE AND GRAVE
<Multi_key> <grave> <dead_breve> <A>		: "Ằ"	U1EB0 # LATIN CAPITAL LETTER A WITH BREVE AND GRAVE
<Multi_key> <grave> <b> <A>			: "Ằ"	U1EB0 # LATIN CAPITAL LETTER A WITH BREVE AND GRAVE
<dead_grave> <abreve>				: "ằ"	U1EB1 # LATIN SMALL LETTER A WITH BREVE AND GRAVE
<Multi_key> <grave> <abreve>			: "ằ"	U1EB1 # LATIN SMALL LETTER A WITH BREVE AND GRAVE
<dead_grave> <dead_breve> <a>			: "ằ"	U1EB1 # LATIN SMALL LETTER A WITH BREVE AND GRAVE
<dead_grave> <Multi_key> <U> <a>		: "ằ"	U1EB1 # LATIN SMALL LETTER A WITH BREVE AND GRAVE
<dead_grave> <Multi_key> <b> <a>		: "ằ"	U1EB1 # LATIN SMALL LETTER A WITH BREVE AND GRAVE
<Multi_key> <grave> <dead_breve> <a>		: "ằ"	U1EB1 # LATIN SMALL LETTER A WITH BREVE AND GRAVE
<Multi_key> <grave> <b> <a>			: "ằ"	U1EB1 # LATIN SMALL LETTER A WITH BREVE AND GRAVE
<dead_hook> <Abreve>				: "Ẳ"	U1EB2 # LATIN CAPITAL LETTER A WITH BREVE AND HOOK ABOVE
<Multi_key> <question> <Abreve>			: "Ẳ"	U1EB2 # LATIN CAPITAL LETTER A WITH BREVE AND HOOK ABOVE
<dead_hook> <dead_breve> <A>			: "Ẳ"	U1EB2 # LATIN CAPITAL LETTER A WITH BREVE AND HOOK ABOVE
<dead_hook> <Multi_key> <U> <A>			: "Ẳ"	U1EB2 # LATIN CAPITAL LETTER A WITH BREVE AND HOOK ABOVE
<dead_hook> <Multi_key> <b> <A>			: "Ẳ"	U1EB2 # LATIN CAPITAL LETTER A WITH BREVE AND HOOK ABOVE
<Multi_key> <question> <dead_breve> <A>		: "Ẳ"	U1EB2 # LATIN CAPITAL LETTER A WITH BREVE AND HOOK ABOVE
<Multi_key> <question> <b> <A>			: "Ẳ"	U1EB2 # LATIN CAPITAL LETTER A WITH BREVE AND HOOK ABOVE
<dead_hook> <abreve>				: "ẳ"	U1EB3 # LATIN SMALL LETTER A WITH BREVE AND HOOK ABOVE
<Multi_key> <question> <abreve>			: "ẳ"	U1EB3 # LATIN SMALL LETTER A WITH BREVE AND HOOK ABOVE
<dead_hook> <dead_breve> <a>			: "ẳ"	U1EB3 # LATIN SMALL LETTER A WITH BREVE AND HOOK ABOVE
<dead_hook> <Multi_key> <U> <a>			: "ẳ"	U1EB3 # LATIN SMALL LETTER A WITH BREVE AND HOOK ABOVE
<dead_hook> <Multi_key> <b> <a>			: "ẳ"	U1EB3 # LATIN SMALL LETTER A WITH BREVE AND HOOK ABOVE
<Multi_key> <question> <dead_breve> <a>		: "ẳ"	U1EB3 # LATIN SMALL LETTER A WITH BREVE AND HOOK ABOVE
<Multi_key> <question> <b> <a>			: "ẳ"	U1EB3 # LATIN SMALL LETTER A WITH BREVE AND HOOK ABOVE
<dead_tilde> <Abreve>				: "Ẵ"	U1EB4 # LATIN CAPITAL LETTER A WITH BREVE AND TILDE
<Multi_key> <asciitilde> <Abreve>		: "Ẵ"	U1EB4 # LATIN CAPITAL LETTER A WITH BREVE AND TILDE
<dead_tilde> <dead_breve> <A>			: "Ẵ"	U1EB4 # LATIN CAPITAL LETTER A WITH BREVE AND TILDE
<dead_tilde> <Multi_key> <U> <A>		: "Ẵ"	U1EB4 # LATIN CAPITAL LETTER A WITH BREVE AND TILDE
<dead_tilde> <Multi_key> <b> <A>		: "Ẵ"	U1EB4 # LATIN CAPITAL LETTER A WITH BREVE AND TILDE
<Multi_key> <asciitilde> <dead_breve> <A>	: "Ẵ"	U1EB4 # LATIN CAPITAL LETTER A WITH BREVE AND TILDE
<Multi_key> <asciitilde> <b> <A>		: "Ẵ"	U1EB4 # LATIN CAPITAL LETTER A WITH BREVE AND TILDE
<dead_tilde> <abreve>				: "ẵ"	U1EB5 # LATIN SMALL LETTER A WITH BREVE AND TILDE
<Multi_key> <asciitilde> <abreve>		: "ẵ"	U1EB5 # LATIN SMALL LETTER A WITH BREVE AND TILDE
<dead_tilde> <dead_breve> <a>			: "ẵ"	U1EB5 # LATIN SMALL LETTER A WITH BREVE AND TILDE
<dead_tilde> <Multi_key> <U> <a>		: "ẵ"	U1EB5 # LATIN SMALL LETTER A WITH BREVE AND TILDE
<dead_tilde> <Multi_key> <b> <a>		: "ẵ"	U1EB5 # LATIN SMALL LETTER A WITH BREVE AND TILDE
<Multi_key> <asciitilde> <dead_breve> <a>	: "ẵ"	U1EB5 # LATIN SMALL LETTER A WITH BREVE AND TILDE
<Multi_key> <asciitilde> <b> <a>		: "ẵ"	U1EB5 # LATIN SMALL LETTER A WITH BREVE AND TILDE
<dead_breve> <dead_belowdot> <A>		: "Ặ"	U1EB6 # LATIN CAPITAL LETTER A WITH BREVE AND DOT BELOW
<dead_breve> <Multi_key> <exclam> <A>		: "Ặ"	U1EB6 # LATIN CAPITAL LETTER A WITH BREVE AND DOT BELOW
<Multi_key> <U> <dead_belowdot> <A>		: "Ặ"	U1EB6 # LATIN CAPITAL LETTER A WITH BREVE AND DOT BELOW
<Multi_key> <U> <exclam> <A>			: "Ặ"	U1EB6 # LATIN CAPITAL LETTER A WITH BREVE AND DOT BELOW
<Multi_key> <b> <dead_belowdot> <A>		: "Ặ"	U1EB6 # LATIN CAPITAL LETTER A WITH BREVE AND DOT BELOW
<Multi_key> <b> <exclam> <A>			: "Ặ"	U1EB6 # LATIN CAPITAL LETTER A WITH BREVE AND DOT BELOW
<dead_belowdot> <Abreve>			: "Ặ"	U1EB6 # LATIN CAPITAL LETTER A WITH BREVE AND DOT BELOW
<dead_breve> <dead_belowdot> <a>		: "ặ"	U1EB7 # LATIN SMALL LETTER A WITH BREVE AND DOT BELOW
<dead_breve> <Multi_key> <exclam> <a>		: "ặ"	U1EB7 # LATIN SMALL LETTER A WITH BREVE AND DOT BELOW
<Multi_key> <U> <dead_belowdot> <a>		: "ặ"	U1EB7 # LATIN SMALL LETTER A WITH BREVE AND DOT BELOW
<Multi_key> <U> <exclam> <a>			: "ặ"	U1EB7 # LATIN SMALL LETTER A WITH BREVE AND DOT BELOW
<Multi_key> <b> <dead_belowdot> <a>		: "ặ"	U1EB7 # LATIN SMALL LETTER A WITH BREVE AND DOT BELOW
<Multi_key> <b> <exclam> <a>			: "ặ"	U1EB7 # LATIN SMALL LETTER A WITH BREVE AND DOT BELOW
<dead_belowdot> <abreve>			: "ặ"	U1EB7 # LATIN SMALL LETTER A WITH BREVE AND DOT BELOW
<dead_belowdot> <E>				: "Ẹ"	U1EB8 # LATIN CAPITAL LETTER E WITH DOT BELOW
<Multi_key> <exclam> <E>			: "Ẹ"	U1EB8 # LATIN CAPITAL LETTER E WITH DOT BELOW
<dead_belowdot> <e>				: "ẹ"	U1EB9 # LATIN SMALL LETTER E WITH DOT BELOW
<Multi_key> <exclam> <e>			: "ẹ"	U1EB9 # LATIN SMALL LETTER E WITH DOT BELOW
<dead_hook> <E>					: "Ẻ"	U1EBA # LATIN CAPITAL LETTER E WITH HOOK ABOVE
<Multi_key> <question> <E>			: "Ẻ"	U1EBA # LATIN CAPITAL LETTER E WITH HOOK ABOVE
<dead_hook> <e>					: "ẻ"	U1EBB # LATIN SMALL LETTER E WITH HOOK ABOVE
<Multi_key> <question> <e>			: "ẻ"	U1EBB # LATIN SMALL LETTER E WITH HOOK ABOVE
<dead_tilde> <E>				: "Ẽ"	U1EBC # LATIN CAPITAL LETTER E WITH TILDE
<Multi_key> <asciitilde> <E>			: "Ẽ"	U1EBC # LATIN CAPITAL LETTER E WITH TILDE
<dead_tilde> <e>				: "ẽ"	U1EBD # LATIN SMALL LETTER E WITH TILDE
<Multi_key> <asciitilde> <e>			: "ẽ"	U1EBD # LATIN SMALL LETTER E WITH TILDE
<dead_acute> <Ecircumflex>			: "Ế"	U1EBE # LATIN CAPITAL LETTER E WITH CIRCUMFLEX AND ACUTE
<Multi_key> <acute> <Ecircumflex>		: "Ế"	U1EBE # LATIN CAPITAL LETTER E WITH CIRCUMFLEX AND ACUTE
<Multi_key> <apostrophe> <Ecircumflex>		: "Ế"	U1EBE # LATIN CAPITAL LETTER E WITH CIRCUMFLEX AND ACUTE
<dead_acute> <dead_circumflex> <E>		: "Ế"	U1EBE # LATIN CAPITAL LETTER E WITH CIRCUMFLEX AND ACUTE
<dead_acute> <Multi_key> <asciicircum> <E>	: "Ế"	U1EBE # LATIN CAPITAL LETTER E WITH CIRCUMFLEX AND ACUTE
<Multi_key> <acute> <dead_circumflex> <E>	: "Ế"	U1EBE # LATIN CAPITAL LETTER E WITH CIRCUMFLEX AND ACUTE
<Multi_key> <acute> <asciicircum> <E>		: "Ế"	U1EBE # LATIN CAPITAL LETTER E WITH CIRCUMFLEX AND ACUTE
<Multi_key> <apostrophe> <dead_circumflex> <E>	: "Ế"	U1EBE # LATIN CAPITAL LETTER E WITH CIRCUMFLEX AND ACUTE
<Multi_key> <apostrophe> <asciicircum> <E>	: "Ế"	U1EBE # LATIN CAPITAL LETTER E WITH CIRCUMFLEX AND ACUTE
<dead_acute> <ecircumflex>			: "ế"	U1EBF # LATIN SMALL LETTER E WITH CIRCUMFLEX AND ACUTE
<Multi_key> <acute> <ecircumflex>		: "ế"	U1EBF # LATIN SMALL LETTER E WITH CIRCUMFLEX AND ACUTE
<Multi_key> <apostrophe> <ecircumflex>		: "ế"	U1EBF # LATIN SMALL LETTER E WITH CIRCUMFLEX AND ACUTE
<dead_acute> <dead_circumflex> <e>		: "ế"	U1EBF # LATIN SMALL LETTER E WITH CIRCUMFLEX AND ACUTE
<dead_acute> <Multi_key> <asciicircum> <e>	: "ế"	U1EBF # LATIN SMALL LETTER E WITH CIRCUMFLEX AND ACUTE
<Multi_key> <acute> <dead_circumflex> <e>	: "ế"	U1EBF # LATIN SMALL LETTER E WITH CIRCUMFLEX AND ACUTE
<Multi_key> <acute> <asciicircum> <e>		: "ế"	U1EBF # LATIN SMALL LETTER E WITH CIRCUMFLEX AND ACUTE
<Multi_key> <apostrophe> <dead_circumflex> <e>	: "ế"	U1EBF # LATIN SMALL LETTER E WITH CIRCUMFLEX AND ACUTE
<Multi_key> <apostrophe> <asciicircum> <e>	: "ế"	U1EBF # LATIN SMALL LETTER E WITH CIRCUMFLEX AND ACUTE
<dead_grave> <Ecircumflex>			: "Ề"	U1EC0 # LATIN CAPITAL LETTER E WITH CIRCUMFLEX AND GRAVE
<Multi_key> <grave> <Ecircumflex>		: "Ề"	U1EC0 # LATIN CAPITAL LETTER E WITH CIRCUMFLEX AND GRAVE
<dead_grave> <dead_circumflex> <E>		: "Ề"	U1EC0 # LATIN CAPITAL LETTER E WITH CIRCUMFLEX AND GRAVE
<dead_grave> <Multi_key> <asciicircum> <E>	: "Ề"	U1EC0 # LATIN CAPITAL LETTER E WITH CIRCUMFLEX AND GRAVE
<Multi_key> <grave> <dead_circumflex> <E>	: "Ề"	U1EC0 # LATIN CAPITAL LETTER E WITH CIRCUMFLEX AND GRAVE
<Multi_key> <grave> <asciicircum> <E>		: "Ề"	U1EC0 # LATIN CAPITAL LETTER E WITH CIRCUMFLEX AND GRAVE
<dead_grave> <ecircumflex>			: "ề"	U1EC1 # LATIN SMALL LETTER E WITH CIRCUMFLEX AND GRAVE
<Multi_key> <grave> <ecircumflex>		: "ề"	U1EC1 # LATIN SMALL LETTER E WITH CIRCUMFLEX AND GRAVE
<dead_grave> <dead_circumflex> <e>		: "ề"	U1EC1 # LATIN SMALL LETTER E WITH CIRCUMFLEX AND GRAVE
<dead_grave> <Multi_key> <asciicircum> <e>	: "ề"	U1EC1 # LATIN SMALL LETTER E WITH CIRCUMFLEX AND GRAVE
<Multi_key> <grave> <dead_circumflex> <e>	: "ề"	U1EC1 # LATIN SMALL LETTER E WITH CIRCUMFLEX AND GRAVE
<Multi_key> <grave> <asciicircum> <e>		: "ề"	U1EC1 # LATIN SMALL LETTER E WITH CIRCUMFLEX AND GRAVE
<dead_hook> <Ecircumflex>			: "Ể"	U1EC2 # LATIN CAPITAL LETTER E WITH CIRCUMFLEX AND HOOK ABOVE
<Multi_key> <question> <Ecircumflex>		: "Ể"	U1EC2 # LATIN CAPITAL LETTER E WITH CIRCUMFLEX AND HOOK ABOVE
<dead_hook> <dead_circumflex> <E>		: "Ể"	U1EC2 # LATIN CAPITAL LETTER E WITH CIRCUMFLEX AND HOOK ABOVE
<dead_hook> <Multi_key> <asciicircum> <E>	: "Ể"	U1EC2 # LATIN CAPITAL LETTER E WITH CIRCUMFLEX AND HOOK ABOVE
<Multi_key> <question> <dead_circumflex> <E>	: "Ể"	U1EC2 # LATIN CAPITAL LETTER E WITH CIRCUMFLEX AND HOOK ABOVE
<Multi_key> <question> <asciicircum> <E>	: "Ể"	U1EC2 # LATIN CAPITAL LETTER E WITH CIRCUMFLEX AND HOOK ABOVE
<dead_hook> <ecircumflex>			: "ể"	U1EC3 # LATIN SMALL LETTER E WITH CIRCUMFLEX AND HOOK ABOVE
<Multi_key> <question> <ecircumflex>		: "ể"	U1EC3 # LATIN SMALL LETTER E WITH CIRCUMFLEX AND HOOK ABOVE
<dead_hook> <dead_circumflex> <e>		: "ể"	U1EC3 # LATIN SMALL LETTER E WITH CIRCUMFLEX AND HOOK ABOVE
<dead_hook> <Multi_key> <asciicircum> <e>	: "ể"	U1EC3 # LATIN SMALL LETTER E WITH CIRCUMFLEX AND HOOK ABOVE
<Multi_key> <question> <dead_circumflex> <e>	: "ể"	U1EC3 # LATIN SMALL LETTER E WITH CIRCUMFLEX AND HOOK ABOVE
<Multi_key> <question> <asciicircum> <e>	: "ể"	U1EC3 # LATIN SMALL LETTER E WITH CIRCUMFLEX AND HOOK ABOVE
<dead_tilde> <Ecircumflex>			: "Ễ"	U1EC4 # LATIN CAPITAL LETTER E WITH CIRCUMFLEX AND TILDE
<Multi_key> <asciitilde> <Ecircumflex>		: "Ễ"	U1EC4 # LATIN CAPITAL LETTER E WITH CIRCUMFLEX AND TILDE
<dead_tilde> <dead_circumflex> <E>		: "Ễ"	U1EC4 # LATIN CAPITAL LETTER E WITH CIRCUMFLEX AND TILDE
<dead_tilde> <Multi_key> <asciicircum> <E>	: "Ễ"	U1EC4 # LATIN CAPITAL LETTER E WITH CIRCUMFLEX AND TILDE
<Multi_key> <asciitilde> <dead_circumflex> <E>	: "Ễ"	U1EC4 # LATIN CAPITAL LETTER E WITH CIRCUMFLEX AND TILDE
<Multi_key> <asciitilde> <asciicircum> <E>	: "Ễ"	U1EC4 # LATIN CAPITAL LETTER E WITH CIRCUMFLEX AND TILDE
<dead_tilde> <ecircumflex>			: "ễ"	U1EC5 # LATIN SMALL LETTER E WITH CIRCUMFLEX AND TILDE
<Multi_key> <asciitilde> <ecircumflex>		: "ễ"	U1EC5 # LATIN SMALL LETTER E WITH CIRCUMFLEX AND TILDE
<dead_tilde> <dead_circumflex> <e>		: "ễ"	U1EC5 # LATIN SMALL LETTER E WITH CIRCUMFLEX AND TILDE
<dead_tilde> <Multi_key> <asciicircum> <e>	: "ễ"	U1EC5 # LATIN SMALL LETTER E WITH CIRCUMFLEX AND TILDE
<Multi_key> <asciitilde> <dead_circumflex> <e>	: "ễ"	U1EC5 # LATIN SMALL LETTER E WITH CIRCUMFLEX AND TILDE
<Multi_key> <asciitilde> <asciicircum> <e>	: "ễ"	U1EC5 # LATIN SMALL LETTER E WITH CIRCUMFLEX AND TILDE
<dead_circumflex> <U1EB8>			: "Ệ"	U1EC6 # LATIN CAPITAL LETTER E WITH CIRCUMFLEX AND DOT BELOW
<Multi_key> <asciicircum> <U1EB8>		: "Ệ"	U1EC6 # LATIN CAPITAL LETTER E WITH CIRCUMFLEX AND DOT BELOW
<dead_circumflex> <dead_belowdot> <E>		: "Ệ"	U1EC6 # LATIN CAPITAL LETTER E WITH CIRCUMFLEX AND DOT BELOW
<dead_circumflex> <Multi_key> <exclam> <E>	: "Ệ"	U1EC6 # LATIN CAPITAL LETTER E WITH CIRCUMFLEX AND DOT BELOW
<Multi_key> <asciicircum> <dead_belowdot> <E>	: "Ệ"	U1EC6 # LATIN CAPITAL LETTER E WITH CIRCUMFLEX AND DOT BELOW
<Multi_key> <asciicircum> <exclam> <E>		: "Ệ"	U1EC6 # LATIN CAPITAL LETTER E WITH CIRCUMFLEX AND DOT BELOW
<dead_belowdot> <Ecircumflex>			: "Ệ"	U1EC6 # LATIN CAPITAL LETTER E WITH CIRCUMFLEX AND DOT BELOW
<dead_circumflex> <U1EB9>			: "ệ"	U1EC7 # LATIN SMALL LETTER E WITH CIRCUMFLEX AND DOT BELOW
<Multi_key> <asciicircum> <U1EB9>		: "ệ"	U1EC7 # LATIN SMALL LETTER E WITH CIRCUMFLEX AND DOT BELOW
<dead_circumflex> <dead_belowdot> <e>		: "ệ"	U1EC7 # LATIN SMALL LETTER E WITH CIRCUMFLEX AND DOT BELOW
<dead_circumflex> <Multi_key> <exclam> <e>	: "ệ"	U1EC7 # LATIN SMALL LETTER E WITH CIRCUMFLEX AND DOT BELOW
<Multi_key> <asciicircum> <dead_belowdot> <e>	: "ệ"	U1EC7 # LATIN SMALL LETTER E WITH CIRCUMFLEX AND DOT BELOW
<Multi_key> <asciicircum> <exclam> <e>		: "ệ"	U1EC7 # LATIN SMALL LETTER E WITH CIRCUMFLEX AND DOT BELOW
<dead_belowdot> <ecircumflex>			: "ệ"	U1EC7 # LATIN SMALL LETTER E WITH CIRCUMFLEX AND DOT BELOW
<dead_hook> <I>					: "Ỉ"	U1EC8 # LATIN CAPITAL LETTER I WITH HOOK ABOVE
<Multi_key> <question> <I>			: "Ỉ"	U1EC8 # LATIN CAPITAL LETTER I WITH HOOK ABOVE
<dead_hook> <i>					: "ỉ"	U1EC9 # LATIN SMALL LETTER I WITH HOOK ABOVE
<Multi_key> <question> <i>			: "ỉ"	U1EC9 # LATIN SMALL LETTER I WITH HOOK ABOVE
<dead_belowdot> <I>				: "Ị"	U1ECA # LATIN CAPITAL LETTER I WITH DOT BELOW
<Multi_key> <exclam> <I>			: "Ị"	U1ECA # LATIN CAPITAL LETTER I WITH DOT BELOW
<dead_belowdot> <i>				: "ị"	U1ECB # LATIN SMALL LETTER I WITH DOT BELOW
<Multi_key> <exclam> <i>			: "ị"	U1ECB # LATIN SMALL LETTER I WITH DOT BELOW
<dead_belowdot> <O>				: "Ọ"	U1ECC # LATIN CAPITAL LETTER O WITH DOT BELOW
<Multi_key> <exclam> <O>			: "Ọ"	U1ECC # LATIN CAPITAL LETTER O WITH DOT BELOW
<dead_belowdot> <o>				: "ọ"	U1ECD # LATIN SMALL LETTER O WITH DOT BELOW
<Multi_key> <exclam> <o>			: "ọ"	U1ECD # LATIN SMALL LETTER O WITH DOT BELOW
<dead_hook> <O>					: "Ỏ"	U1ECE # LATIN CAPITAL LETTER O WITH HOOK ABOVE
<Multi_key> <question> <O>			: "Ỏ"	U1ECE # LATIN CAPITAL LETTER O WITH HOOK ABOVE
<dead_hook> <o>					: "ỏ"	U1ECF # LATIN SMALL LETTER O WITH HOOK ABOVE
<Multi_key> <question> <o>			: "ỏ"	U1ECF # LATIN SMALL LETTER O WITH HOOK ABOVE
<dead_acute> <Ocircumflex>			: "Ố"	U1ED0 # LATIN CAPITAL LETTER O WITH CIRCUMFLEX AND ACUTE
<Multi_key> <acute> <Ocircumflex>		: "Ố"	U1ED0 # LATIN CAPITAL LETTER O WITH CIRCUMFLEX AND ACUTE
<Multi_key> <apostrophe> <Ocircumflex>		: "Ố"	U1ED0 # LATIN CAPITAL LETTER O WITH CIRCUMFLEX AND ACUTE
<dead_acute> <dead_circumflex> <O>		: "Ố"	U1ED0 # LATIN CAPITAL LETTER O WITH CIRCUMFLEX AND ACUTE
<dead_acute> <Multi_key> <asciicircum> <O>	: "Ố"	U1ED0 # LATIN CAPITAL LETTER O WITH CIRCUMFLEX AND ACUTE
<Multi_key> <acute> <dead_circumflex> <O>	: "Ố"	U1ED0 # LATIN CAPITAL LETTER O WITH CIRCUMFLEX AND ACUTE
<Multi_key> <acute> <asciicircum> <O>		: "Ố"	U1ED0 # LATIN CAPITAL LETTER O WITH CIRCUMFLEX AND ACUTE
<Multi_key> <apostrophe> <dead_circumflex> <O>	: "Ố"	U1ED0 # LATIN CAPITAL LETTER O WITH CIRCUMFLEX AND ACUTE
<Multi_key> <apostrophe> <asciicircum> <O>	: "Ố"	U1ED0 # LATIN CAPITAL LETTER O WITH CIRCUMFLEX AND ACUTE
<dead_acute> <ocircumflex>			: "ố"	U1ED1 # LATIN SMALL LETTER O WITH CIRCUMFLEX AND ACUTE
<Multi_key> <acute> <ocircumflex>		: "ố"	U1ED1 # LATIN SMALL LETTER O WITH CIRCUMFLEX AND ACUTE
<Multi_key> <apostrophe> <ocircumflex>		: "ố"	U1ED1 # LATIN SMALL LETTER O WITH CIRCUMFLEX AND ACUTE
<dead_acute> <dead_circumflex> <o>		: "ố"	U1ED1 # LATIN SMALL LETTER O WITH CIRCUMFLEX AND ACUTE
<dead_acute> <Multi_key> <asciicircum> <o>	: "ố"	U1ED1 # LATIN SMALL LETTER O WITH CIRCUMFLEX AND ACUTE
<Multi_key> <acute> <dead_circumflex> <o>	: "ố"	U1ED1 # LATIN SMALL LETTER O WITH CIRCUMFLEX AND ACUTE
<Multi_key> <acute> <asciicircum> <o>		: "ố"	U1ED1 # LATIN SMALL LETTER O WITH CIRCUMFLEX AND ACUTE
<Multi_key> <apostrophe> <dead_circumflex> <o>	: "ố"	U1ED1 # LATIN SMALL LETTER O WITH CIRCUMFLEX AND ACUTE
<Multi_key> <apostrophe> <asciicircum> <o>	: "ố"	U1ED1 # LATIN SMALL LETTER O WITH CIRCUMFLEX AND ACUTE
<dead_grave> <Ocircumflex>			: "Ồ"	U1ED2 # LATIN CAPITAL LETTER O WITH CIRCUMFLEX AND GRAVE
<Multi_key> <grave> <Ocircumflex>		: "Ồ"	U1ED2 # LATIN CAPITAL LETTER O WITH CIRCUMFLEX AND GRAVE
<dead_grave> <dead_circumflex> <O>		: "Ồ"	U1ED2 # LATIN CAPITAL LETTER O WITH CIRCUMFLEX AND GRAVE
<dead_grave> <Multi_key> <asciicircum> <O>	: "Ồ"	U1ED2 # LATIN CAPITAL LETTER O WITH CIRCUMFLEX AND GRAVE
<Multi_key> <grave> <dead_circumflex> <O>	: "Ồ"	U1ED2 # LATIN CAPITAL LETTER O WITH CIRCUMFLEX AND GRAVE
<Multi_key> <grave> <asciicircum> <O>		: "Ồ"	U1ED2 # LATIN CAPITAL LETTER O WITH CIRCUMFLEX AND GRAVE
<dead_grave> <ocircumflex>			: "ồ"	U1ED3 # LATIN SMALL LETTER O WITH CIRCUMFLEX AND GRAVE
<Multi_key> <grave> <ocircumflex>		: "ồ"	U1ED3 # LATIN SMALL LETTER O WITH CIRCUMFLEX AND GRAVE
<dead_grave> <dead_circumflex> <o>		: "ồ"	U1ED3 # LATIN SMALL LETTER O WITH CIRCUMFLEX AND GRAVE
<dead_grave> <Multi_key> <asciicircum> <o>	: "ồ"	U1ED3 # LATIN SMALL LETTER O WITH CIRCUMFLEX AND GRAVE
<Multi_key> <grave> <dead_circumflex> <o>	: "ồ"	U1ED3 # LATIN SMALL LETTER O WITH CIRCUMFLEX AND GRAVE
<Multi_key> <grave> <asciicircum> <o>		: "ồ"	U1ED3 # LATIN SMALL LETTER O WITH CIRCUMFLEX AND GRAVE
<dead_hook> <Ocircumflex>			: "Ổ"	U1ED4 # LATIN CAPITAL LETTER O WITH CIRCUMFLEX AND HOOK ABOVE
<Multi_key> <question> <Ocircumflex>		: "Ổ"	U1ED4 # LATIN CAPITAL LETTER O WITH CIRCUMFLEX AND HOOK ABOVE
<dead_hook> <dead_circumflex> <O>		: "Ổ"	U1ED4 # LATIN CAPITAL LETTER O WITH CIRCUMFLEX AND HOOK ABOVE
<dead_hook> <Multi_key> <asciicircum> <O>	: "Ổ"	U1ED4 # LATIN CAPITAL LETTER O WITH CIRCUMFLEX AND HOOK ABOVE
<Multi_key> <question> <dead_circumflex> <O>	: "Ổ"	U1ED4 # LATIN CAPITAL LETTER O WITH CIRCUMFLEX AND HOOK ABOVE
<Multi_key> <question> <asciicircum> <O>	: "Ổ"	U1ED4 # LATIN CAPITAL LETTER O WITH CIRCUMFLEX AND HOOK ABOVE
<dead_hook> <ocircumflex>			: "ổ"	U1ED5 # LATIN SMALL LETTER O WITH CIRCUMFLEX AND HOOK ABOVE
<Multi_key> <question> <ocircumflex>		: "ổ"	U1ED5 # LATIN SMALL LETTER O WITH CIRCUMFLEX AND HOOK ABOVE
<dead_hook> <dead_circumflex> <o>		: "ổ"	U1ED5 # LATIN SMALL LETTER O WITH CIRCUMFLEX AND HOOK ABOVE
<dead_hook> <Multi_key> <asciicircum> <o>	: "ổ"	U1ED5 # LATIN SMALL LETTER O WITH CIRCUMFLEX AND HOOK ABOVE
<Multi_key> <question> <dead_circumflex> <o>	: "ổ"	U1ED5 # LATIN SMALL LETTER O WITH CIRCUMFLEX AND HOOK ABOVE
<Multi_key> <question> <asciicircum> <o>	: "ổ"	U1ED5 # LATIN SMALL LETTER O WITH CIRCUMFLEX AND HOOK ABOVE
<dead_tilde> <Ocircumflex>			: "Ỗ"	U1ED6 # LATIN CAPITAL LETTER O WITH CIRCUMFLEX AND TILDE
<Multi_key> <asciitilde> <Ocircumflex>		: "Ỗ"	U1ED6 # LATIN CAPITAL LETTER O WITH CIRCUMFLEX AND TILDE
<dead_tilde> <dead_circumflex> <O>		: "Ỗ"	U1ED6 # LATIN CAPITAL LETTER O WITH CIRCUMFLEX AND TILDE
<dead_tilde> <Multi_key> <asciicircum> <O>	: "Ỗ"	U1ED6 # LATIN CAPITAL LETTER O WITH CIRCUMFLEX AND TILDE
<Multi_key> <asciitilde> <dead_circumflex> <O>	: "Ỗ"	U1ED6 # LATIN CAPITAL LETTER O WITH CIRCUMFLEX AND TILDE
<Multi_key> <asciitilde> <asciicircum> <O>	: "Ỗ"	U1ED6 # LATIN CAPITAL LETTER O WITH CIRCUMFLEX AND TILDE
<dead_tilde> <ocircumflex>			: "ỗ"	U1ED7 # LATIN SMALL LETTER O WITH CIRCUMFLEX AND TILDE
<Multi_key> <asciitilde> <ocircumflex>		: "ỗ"	U1ED7 # LATIN SMALL LETTER O WITH CIRCUMFLEX AND TILDE
<dead_tilde> <dead_circumflex> <o>		: "ỗ"	U1ED7 # LATIN SMALL LETTER O WITH CIRCUMFLEX AND TILDE
<dead_tilde> <Multi_key> <asciicircum> <o>	: "ỗ"	U1ED7 # LATIN SMALL LETTER O WITH CIRCUMFLEX AND TILDE
<Multi_key> <asciitilde> <dead_circumflex> <o>	: "ỗ"	U1ED7 # LATIN SMALL LETTER O WITH CIRCUMFLEX AND TILDE
<Multi_key> <asciitilde> <asciicircum> <o>	: "ỗ"	U1ED7 # LATIN SMALL LETTER O WITH CIRCUMFLEX AND TILDE
<dead_circumflex> <U1ECC>			: "Ộ"	U1ED8 # LATIN CAPITAL LETTER O WITH CIRCUMFLEX AND DOT BELOW
<Multi_key> <asciicircum> <U1ECC>		: "Ộ"	U1ED8 # LATIN CAPITAL LETTER O WITH CIRCUMFLEX AND DOT BELOW
<dead_circumflex> <dead_belowdot> <O>		: "Ộ"	U1ED8 # LATIN CAPITAL LETTER O WITH CIRCUMFLEX AND DOT BELOW
<dead_circumflex> <Multi_key> <exclam> <O>	: "Ộ"	U1ED8 # LATIN CAPITAL LETTER O WITH CIRCUMFLEX AND DOT BELOW
<Multi_key> <asciicircum> <dead_belowdot> <O>	: "Ộ"	U1ED8 # LATIN CAPITAL LETTER O WITH CIRCUMFLEX AND DOT BELOW
<Multi_key> <asciicircum> <exclam> <O>		: "Ộ"	U1ED8 # LATIN CAPITAL LETTER O WITH CIRCUMFLEX AND DOT BELOW
<dead_belowdot> <Ocircumflex>			: "Ộ"	U1ED8 # LATIN CAPITAL LETTER O WITH CIRCUMFLEX AND DOT BELOW
<dead_circumflex> <U1ECD>			: "ộ"	U1ED9 # LATIN SMALL LETTER O WITH CIRCUMFLEX AND DOT BELOW
<Multi_key> <asciicircum> <U1ECD>		: "ộ"	U1ED9 # LATIN SMALL LETTER O WITH CIRCUMFLEX AND DOT BELOW
<dead_circumflex> <dead_belowdot> <o>		: "ộ"	U1ED9 # LATIN SMALL LETTER O WITH CIRCUMFLEX AND DOT BELOW
<dead_circumflex> <Multi_key> <exclam> <o>	: "ộ"	U1ED9 # LATIN SMALL LETTER O WITH CIRCUMFLEX AND DOT BELOW
<Multi_key> <asciicircum> <dead_belowdot> <o>	: "ộ"	U1ED9 # LATIN SMALL LETTER O WITH CIRCUMFLEX AND DOT BELOW
<Multi_key> <asciicircum> <exclam> <o>		: "ộ"	U1ED9 # LATIN SMALL LETTER O WITH CIRCUMFLEX AND DOT BELOW
<dead_belowdot> <ocircumflex>			: "ộ"	U1ED9 # LATIN SMALL LETTER O WITH CIRCUMFLEX AND DOT BELOW
<dead_acute> <Ohorn>				: "Ớ"	U1EDA # LATIN CAPITAL LETTER O WITH HORN AND ACUTE
<Multi_key> <acute> <Ohorn>			: "Ớ"	U1EDA # LATIN CAPITAL LETTER O WITH HORN AND ACUTE
<Multi_key> <apostrophe> <Ohorn>		: "Ớ"	U1EDA # LATIN CAPITAL LETTER O WITH HORN AND ACUTE
<dead_acute> <dead_horn> <O>			: "Ớ"	U1EDA # LATIN CAPITAL LETTER O WITH HORN AND ACUTE
<dead_acute> <Multi_key> <plus> <O>		: "Ớ"	U1EDA # LATIN CAPITAL LETTER O WITH HORN AND ACUTE
<Multi_key> <acute> <dead_horn> <O>		: "Ớ"	U1EDA # LATIN CAPITAL LETTER O WITH HORN AND ACUTE
<Multi_key> <acute> <plus> <O>			: "Ớ"	U1EDA # LATIN CAPITAL LETTER O WITH HORN AND ACUTE
<Multi_key> <apostrophe> <dead_horn> <O>	: "Ớ"	U1EDA # LATIN CAPITAL LETTER O WITH HORN AND ACUTE
<Multi_key> <apostrophe> <plus> <O>		: "Ớ"	U1EDA # LATIN CAPITAL LETTER O WITH HORN AND ACUTE
<dead_acute> <ohorn>				: "ớ"	U1EDB # LATIN SMALL LETTER O WITH HORN AND ACUTE
<Multi_key> <acute> <ohorn>			: "ớ"	U1EDB # LATIN SMALL LETTER O WITH HORN AND ACUTE
<Multi_key> <apostrophe> <ohorn>		: "ớ"	U1EDB # LATIN SMALL LETTER O WITH HORN AND ACUTE
<dead_acute> <dead_horn> <o>			: "ớ"	U1EDB # LATIN SMALL LETTER O WITH HORN AND ACUTE
<dead_acute> <Multi_key> <plus> <o>		: "ớ"	U1EDB # LATIN SMALL LETTER O WITH HORN AND ACUTE
<Multi_key> <acute> <dead_horn> <o>		: "ớ"	U1EDB # LATIN SMALL LETTER O WITH HORN AND ACUTE
<Multi_key> <acute> <plus> <o>			: "ớ"	U1EDB # LATIN SMALL LETTER O WITH HORN AND ACUTE
<Multi_key> <apostrophe> <dead_horn> <o>	: "ớ"	U1EDB # LATIN SMALL LETTER O WITH HORN AND ACUTE
<Multi_key> <apostrophe> <plus> <o>		: "ớ"	U1EDB # LATIN SMALL LETTER O WITH HORN AND ACUTE
<dead_grave> <Ohorn>				: "Ờ"	U1EDC # LATIN CAPITAL LETTER O WITH HORN AND GRAVE
<Multi_key> <grave> <Ohorn>			: "Ờ"	U1EDC # LATIN CAPITAL LETTER O WITH HORN AND GRAVE
<dead_grave> <dead_horn> <O>			: "Ờ"	U1EDC # LATIN CAPITAL LETTER O WITH HORN AND GRAVE
<dead_grave> <Multi_key> <plus> <O>		: "Ờ"	U1EDC # LATIN CAPITAL LETTER O WITH HORN AND GRAVE
<Multi_key> <grave> <dead_horn> <O>		: "Ờ"	U1EDC # LATIN CAPITAL LETTER O WITH HORN AND GRAVE
<Multi_key> <grave> <plus> <O>			: "Ờ"	U1EDC # LATIN CAPITAL LETTER O WITH HORN AND GRAVE
<dead_grave> <ohorn>				: "ờ"	U1EDD # LATIN SMALL LETTER O WITH HORN AND GRAVE
<Multi_key> <grave> <ohorn>			: "ờ"	U1EDD # LATIN SMALL LETTER O WITH HORN AND GRAVE
<dead_grave> <dead_horn> <o>			: "ờ"	U1EDD # LATIN SMALL LETTER O WITH HORN AND GRAVE
<dead_grave> <Multi_key> <plus> <o>		: "ờ"	U1EDD # LATIN SMALL LETTER O WITH HORN AND GRAVE
<Multi_key> <grave> <dead_horn> <o>		: "ờ"	U1EDD # LATIN SMALL LETTER O WITH HORN AND GRAVE
<Multi_key> <grave> <plus> <o>			: "ờ"	U1EDD # LATIN SMALL LETTER O WITH HORN AND GRAVE
<dead_hook> <Ohorn>				: "Ở"	U1EDE # LATIN CAPITAL LETTER O WITH HORN AND HOOK ABOVE
<Multi_key> <question> <Ohorn>			: "Ở"	U1EDE # LATIN CAPITAL LETTER O WITH HORN AND HOOK ABOVE
<dead_hook> <dead_horn> <O>			: "Ở"	U1EDE # LATIN CAPITAL LETTER O WITH HORN AND HOOK ABOVE
<dead_hook> <Multi_key> <plus> <O>		: "Ở"	U1EDE # LATIN CAPITAL LETTER O WITH HORN AND HOOK ABOVE
<Multi_key> <question> <dead_horn> <O>		: "Ở"	U1EDE # LATIN CAPITAL LETTER O WITH HORN AND HOOK ABOVE
<Multi_key> <question> <plus> <O>		: "Ở"	U1EDE # LATIN CAPITAL LETTER O WITH HORN AND HOOK ABOVE
<dead_hook> <ohorn>				: "ở"	U1EDF # LATIN SMALL LETTER O WITH HORN AND HOOK ABOVE
<Multi_key> <question> <ohorn>			: "ở"	U1EDF # LATIN SMALL LETTER O WITH HORN AND HOOK ABOVE
<dead_hook> <dead_horn> <o>			: "ở"	U1EDF # LATIN SMALL LETTER O WITH HORN AND HOOK ABOVE
<dead_hook> <Multi_key> <plus> <o>		: "ở"	U1EDF # LATIN SMALL LETTER O WITH HORN AND HOOK ABOVE
<Multi_key> <question> <dead_horn> <o>		: "ở"	U1EDF # LATIN SMALL LETTER O WITH HORN AND HOOK ABOVE
<Multi_key> <question> <plus> <o>		: "ở"	U1EDF # LATIN SMALL LETTER O WITH HORN AND HOOK ABOVE
<dead_tilde> <Ohorn>				: "Ỡ"	U1EE0 # LATIN CAPITAL LETTER O WITH HORN AND TILDE
<Multi_key> <asciitilde> <Ohorn>		: "Ỡ"	U1EE0 # LATIN CAPITAL LETTER O WITH HORN AND TILDE
<dead_tilde> <dead_horn> <O>			: "Ỡ"	U1EE0 # LATIN CAPITAL LETTER O WITH HORN AND TILDE
<dead_tilde> <Multi_key> <plus> <O>		: "Ỡ"	U1EE0 # LATIN CAPITAL LETTER O WITH HORN AND TILDE
<Multi_key> <asciitilde> <dead_horn> <O>	: "Ỡ"	U1EE0 # LATIN CAPITAL LETTER O WITH HORN AND TILDE
<Multi_key> <asciitilde> <plus> <O>		: "Ỡ"	U1EE0 # LATIN CAPITAL LETTER O WITH HORN AND TILDE
<dead_tilde> <ohorn>				: "ỡ"	U1EE1 # LATIN SMALL LETTER O WITH HORN AND TILDE
<Multi_key> <asciitilde> <ohorn>		: "ỡ"	U1EE1 # LATIN SMALL LETTER O WITH HORN AND TILDE
<dead_tilde> <dead_horn> <o>			: "ỡ"	U1EE1 # LATIN SMALL LETTER O WITH HORN AND TILDE
<dead_tilde> <Multi_key> <plus> <o>		: "ỡ"	U1EE1 # LATIN SMALL LETTER O WITH HORN AND TILDE
<Multi_key> <asciitilde> <dead_horn> <o>	: "ỡ"	U1EE1 # LATIN SMALL LETTER O WITH HORN AND TILDE
<Multi_key> <asciitilde> <plus> <o>		: "ỡ"	U1EE1 # LATIN SMALL LETTER O WITH HORN AND TILDE
<dead_belowdot> <Ohorn>				: "Ợ"	U1EE2 # LATIN CAPITAL LETTER O WITH HORN AND DOT BELOW
<Multi_key> <exclam> <Ohorn>			: "Ợ"	U1EE2 # LATIN CAPITAL LETTER O WITH HORN AND DOT BELOW
<dead_belowdot> <dead_horn> <O>			: "Ợ"	U1EE2 # LATIN CAPITAL LETTER O WITH HORN AND DOT BELOW
<dead_belowdot> <Multi_key> <plus> <O>		: "Ợ"	U1EE2 # LATIN CAPITAL LETTER O WITH HORN AND DOT BELOW
<Multi_key> <exclam> <dead_horn> <O>		: "Ợ"	U1EE2 # LATIN CAPITAL LETTER O WITH HORN AND DOT BELOW
<Multi_key> <exclam> <plus> <O>			: "Ợ"	U1EE2 # LATIN CAPITAL LETTER O WITH HORN AND DOT BELOW
<dead_belowdot> <ohorn>				: "ợ"	U1EE3 # LATIN SMALL LETTER O WITH HORN AND DOT BELOW
<Multi_key> <exclam> <ohorn>			: "ợ"	U1EE3 # LATIN SMALL LETTER O WITH HORN AND DOT BELOW
<dead_belowdot> <dead_horn> <o>			: "ợ"	U1EE3 # LATIN SMALL LETTER O WITH HORN AND DOT BELOW
<dead_belowdot> <Multi_key> <plus> <o>		: "ợ"	U1EE3 # LATIN SMALL LETTER O WITH HORN AND DOT BELOW
<Multi_key> <exclam> <dead_horn> <o>		: "ợ"	U1EE3 # LATIN SMALL LETTER O WITH HORN AND DOT BELOW
<Multi_key> <exclam> <plus> <o>			: "ợ"	U1EE3 # LATIN SMALL LETTER O WITH HORN AND DOT BELOW
<dead_belowdot> <U>				: "Ụ"	U1EE4 # LATIN CAPITAL LETTER U WITH DOT BELOW
<Multi_key> <exclam> <U>			: "Ụ"	U1EE4 # LATIN CAPITAL LETTER U WITH DOT BELOW
<dead_belowdot> <u>				: "ụ"	U1EE5 # LATIN SMALL LETTER U WITH DOT BELOW
<Multi_key> <exclam> <u>			: "ụ"	U1EE5 # LATIN SMALL LETTER U WITH DOT BELOW
<dead_hook> <U>					: "Ủ"	U1EE6 # LATIN CAPITAL LETTER U WITH HOOK ABOVE
<Multi_key> <question> <U>			: "Ủ"	U1EE6 # LATIN CAPITAL LETTER U WITH HOOK ABOVE
<dead_hook> <u>					: "ủ"	U1EE7 # LATIN SMALL LETTER U WITH HOOK ABOVE
<Multi_key> <question> <u>			: "ủ"	U1EE7 # LATIN SMALL LETTER U WITH HOOK ABOVE
<dead_acute> <Uhorn>				: "Ứ"	U1EE8 # LATIN CAPITAL LETTER U WITH HORN AND ACUTE
<Multi_key> <acute> <Uhorn>			: "Ứ"	U1EE8 # LATIN CAPITAL LETTER U WITH HORN AND ACUTE
<Multi_key> <apostrophe> <Uhorn>		: "Ứ"	U1EE8 # LATIN CAPITAL LETTER U WITH HORN AND ACUTE
<dead_acute> <dead_horn> <U>			: "Ứ"	U1EE8 # LATIN CAPITAL LETTER U WITH HORN AND ACUTE
<dead_acute> <Multi_key> <plus> <U>		: "Ứ"	U1EE8 # LATIN CAPITAL LETTER U WITH HORN AND ACUTE
<Multi_key> <acute> <dead_horn> <U>		: "Ứ"	U1EE8 # LATIN CAPITAL LETTER U WITH HORN AND ACUTE
<Multi_key> <acute> <plus> <U>			: "Ứ"	U1EE8 # LATIN CAPITAL LETTER U WITH HORN AND ACUTE
<Multi_key> <apostrophe> <dead_horn> <U>	: "Ứ"	U1EE8 # LATIN CAPITAL LETTER U WITH HORN AND ACUTE
<Multi_key> <apostrophe> <plus> <U>		: "Ứ"	U1EE8 # LATIN CAPITAL LETTER U WITH HORN AND ACUTE
<dead_acute> <uhorn>				: "ứ"	U1EE9 # LATIN SMALL LETTER U WITH HORN AND ACUTE
<Multi_key> <acute> <uhorn>			: "ứ"	U1EE9 # LATIN SMALL LETTER U WITH HORN AND ACUTE
<Multi_key> <apostrophe> <uhorn>		: "ứ"	U1EE9 # LATIN SMALL LETTER U WITH HORN AND ACUTE
<dead_acute> <dead_horn> <u>			: "ứ"	U1EE9 # LATIN SMALL LETTER U WITH HORN AND ACUTE
<dead_acute> <Multi_key> <plus> <u>		: "ứ"	U1EE9 # LATIN SMALL LETTER U WITH HORN AND ACUTE
<Multi_key> <acute> <dead_horn> <u>		: "ứ"	U1EE9 # LATIN SMALL LETTER U WITH HORN AND ACUTE
<Multi_key> <acute> <plus> <u>			: "ứ"	U1EE9 # LATIN SMALL LETTER U WITH HORN AND ACUTE
<Multi_key> <apostrophe> <dead_horn> <u>	: "ứ"	U1EE9 # LATIN SMALL LETTER U WITH HORN AND ACUTE
<Multi_key> <apostrophe> <plus> <u>		: "ứ"	U1EE9 # LATIN SMALL LETTER U WITH HORN AND ACUTE
<dead_grave> <Uhorn>				: "Ừ"	U1EEA # LATIN CAPITAL LETTER U WITH HORN AND GRAVE
<Multi_key> <grave> <Uhorn>			: "Ừ"	U1EEA # LATIN CAPITAL LETTER U WITH HORN AND GRAVE
<dead_grave> <dead_horn> <U>			: "Ừ"	U1EEA # LATIN CAPITAL LETTER U WITH HORN AND GRAVE
<dead_grave> <Multi_key> <plus> <U>		: "Ừ"	U1EEA # LATIN CAPITAL LETTER U WITH HORN AND GRAVE
<Multi_key> <grave> <dead_horn> <U>		: "Ừ"	U1EEA # LATIN CAPITAL LETTER U WITH HORN AND GRAVE
<Multi_key> <grave> <plus> <U>			: "Ừ"	U1EEA # LATIN CAPITAL LETTER U WITH HORN AND GRAVE
<dead_grave> <uhorn>				: "ừ"	U1EEB # LATIN SMALL LETTER U WITH HORN AND GRAVE
<Multi_key> <grave> <uhorn>			: "ừ"	U1EEB # LATIN SMALL LETTER U WITH HORN AND GRAVE
<dead_grave> <dead_horn> <u>			: "ừ"	U1EEB # LATIN SMALL LETTER U WITH HORN AND GRAVE
<dead_grave> <Multi_key> <plus> <u>		: "ừ"	U1EEB # LATIN SMALL LETTER U WITH HORN AND GRAVE
<Multi_key> <grave> <dead_horn> <u>		: "ừ"	U1EEB # LATIN SMALL LETTER U WITH HORN AND GRAVE
<Multi_key> <grave> <plus> <u>			: "ừ"	U1EEB # LATIN SMALL LETTER U WITH HORN AND GRAVE
<dead_hook> <Uhorn>				: "Ử"	U1EEC # LATIN CAPITAL LETTER U WITH HORN AND HOOK ABOVE
<Multi_key> <question> <Uhorn>			: "Ử"	U1EEC # LATIN CAPITAL LETTER U WITH HORN AND HOOK ABOVE
<dead_hook> <dead_horn> <U>			: "Ử"	U1EEC # LATIN CAPITAL LETTER U WITH HORN AND HOOK ABOVE
<dead_hook> <Multi_key> <plus> <U>		: "Ử"	U1EEC # LATIN CAPITAL LETTER U WITH HORN AND HOOK ABOVE
<Multi_key> <question> <dead_horn> <U>		: "Ử"	U1EEC # LATIN CAPITAL LETTER U WITH HORN AND HOOK ABOVE
<Multi_key> <question> <plus> <U>		: "Ử"	U1EEC # LATIN CAPITAL LETTER U WITH HORN AND HOOK ABOVE
<dead_hook> <uhorn>				: "ử"	U1EED # LATIN SMALL LETTER U WITH HORN AND HOOK ABOVE
<Multi_key> <question> <uhorn>			: "ử"	U1EED # LATIN SMALL LETTER U WITH HORN AND HOOK ABOVE
<dead_hook> <dead_horn> <u>			: "ử"	U1EED # LATIN SMALL LETTER U WITH HORN AND HOOK ABOVE
<dead_hook> <Multi_key> <plus> <u>		: "ử"	U1EED # LATIN SMALL LETTER U WITH HORN AND HOOK ABOVE
<Multi_key> <question> <dead_horn> <u>		: "ử"	U1EED # LATIN SMALL LETTER U WITH HORN AND HOOK ABOVE
<Multi_key> <question> <plus> <u>		: "ử"	U1EED # LATIN SMALL LETTER U WITH HORN AND HOOK ABOVE
<dead_tilde> <Uhorn>				: "Ữ"	U1EEE # LATIN CAPITAL LETTER U WITH HORN AND TILDE
<Multi_key> <asciitilde> <Uhorn>		: "Ữ"	U1EEE # LATIN CAPITAL LETTER U WITH HORN AND TILDE
<dead_tilde> <dead_horn> <U>			: "Ữ"	U1EEE # LATIN CAPITAL LETTER U WITH HORN AND TILDE
<dead_tilde> <Multi_key> <plus> <U>		: "Ữ"	U1EEE # LATIN CAPITAL LETTER U WITH HORN AND TILDE
<Multi_key> <asciitilde> <dead_horn> <U>	: "Ữ"	U1EEE # LATIN CAPITAL LETTER U WITH HORN AND TILDE
<Multi_key> <asciitilde> <plus> <U>		: "Ữ"	U1EEE # LATIN CAPITAL LETTER U WITH HORN AND TILDE
<dead_tilde> <uhorn>				: "ữ"	U1EEF # LATIN SMALL LETTER U WITH HORN AND TILDE
<Multi_key> <asciitilde> <uhorn>		: "ữ"	U1EEF # LATIN SMALL LETTER U WITH HORN AND TILDE
<dead_tilde> <dead_horn> <u>			: "ữ"	U1EEF # LATIN SMALL LETTER U WITH HORN AND TILDE
<dead_tilde> <Multi_key> <plus> <u>		: "ữ"	U1EEF # LATIN SMALL LETTER U WITH HORN AND TILDE
<Multi_key> <asciitilde> <dead_horn> <u>	: "ữ"	U1EEF # LATIN SMALL LETTER U WITH HORN AND TILDE
<Multi_key> <asciitilde> <plus> <u>		: "ữ"	U1EEF # LATIN SMALL LETTER U WITH HORN AND TILDE
<dead_belowdot> <Uhorn>				: "Ự"	U1EF0 # LATIN CAPITAL LETTER U WITH HORN AND DOT BELOW
<Multi_key> <exclam> <Uhorn>			: "Ự"	U1EF0 # LATIN CAPITAL LETTER U WITH HORN AND DOT BELOW
<dead_belowdot> <dead_horn> <U>			: "Ự"	U1EF0 # LATIN CAPITAL LETTER U WITH HORN AND DOT BELOW
<dead_belowdot> <Multi_key> <plus> <U>		: "Ự"	U1EF0 # LATIN CAPITAL LETTER U WITH HORN AND DOT BELOW
<Multi_key> <exclam> <dead_horn> <U>		: "Ự"	U1EF0 # LATIN CAPITAL LETTER U WITH HORN AND DOT BELOW
<Multi_key> <exclam> <plus> <U>			: "Ự"	U1EF0 # LATIN CAPITAL LETTER U WITH HORN AND DOT BELOW
<dead_belowdot> <uhorn>				: "ự"	U1EF1 # LATIN SMALL LETTER U WITH HORN AND DOT BELOW
<Multi_key> <exclam> <uhorn>			: "ự"	U1EF1 # LATIN SMALL LETTER U WITH HORN AND DOT BELOW
<dead_belowdot> <dead_horn> <u>			: "ự"	U1EF1 # LATIN SMALL LETTER U WITH HORN AND DOT BELOW
<dead_belowdot> <Multi_key> <plus> <u>		: "ự"	U1EF1 # LATIN SMALL LETTER U WITH HORN AND DOT BELOW
<Multi_key> <exclam> <dead_horn> <u>		: "ự"	U1EF1 # LATIN SMALL LETTER U WITH HORN AND DOT BELOW
<Multi_key> <exclam> <plus> <u>			: "ự"	U1EF1 # LATIN SMALL LETTER U WITH HORN AND DOT BELOW
<dead_grave> <Y>				: "Ỳ"	U1EF2 # LATIN CAPITAL LETTER Y WITH GRAVE
<Multi_key> <grave> <Y>				: "Ỳ"	U1EF2 # LATIN CAPITAL LETTER Y WITH GRAVE
<dead_grave> <y>				: "ỳ"	U1EF3 # LATIN SMALL LETTER Y WITH GRAVE
<Multi_key> <grave> <y>				: "ỳ"	U1EF3 # LATIN SMALL LETTER Y WITH GRAVE
<dead_belowdot> <Y>				: "Ỵ"	U1EF4 # LATIN CAPITAL LETTER Y WITH DOT BELOW
<Multi_key> <exclam> <Y>			: "Ỵ"	U1EF4 # LATIN CAPITAL LETTER Y WITH DOT BELOW
<dead_belowdot> <y>				: "ỵ"	U1EF5 # LATIN SMALL LETTER Y WITH DOT BELOW
<Multi_key> <exclam> <y>			: "ỵ"	U1EF5 # LATIN SMALL LETTER Y WITH DOT BELOW
<dead_hook> <Y>					: "Ỷ"	U1EF6 # LATIN CAPITAL LETTER Y WITH HOOK ABOVE
<Multi_key> <question> <Y>			: "Ỷ"	U1EF6 # LATIN CAPITAL LETTER Y WITH HOOK ABOVE
<dead_hook> <y>					: "ỷ"	U1EF7 # LATIN SMALL LETTER Y WITH HOOK ABOVE
<Multi_key> <question> <y>			: "ỷ"	U1EF7 # LATIN SMALL LETTER Y WITH HOOK ABOVE
<dead_tilde> <Y>				: "Ỹ"	U1EF8 # LATIN CAPITAL LETTER Y WITH TILDE
<Multi_key> <asciitilde> <Y>			: "Ỹ"	U1EF8 # LATIN CAPITAL LETTER Y WITH TILDE
<dead_tilde> <y>				: "ỹ"	U1EF9 # LATIN SMALL LETTER Y WITH TILDE
<Multi_key> <asciitilde> <y>			: "ỹ"	U1EF9 # LATIN SMALL LETTER Y WITH TILDE
# Greek Extended
<dead_psili> <Greek_alpha>		: "ἀ"	U1F00 # GREEK SMALL LETTER ALPHA WITH PSILI
<Multi_key> <parenright> <Greek_alpha>	: "ἀ"	U1F00 # GREEK SMALL LETTER ALPHA WITH PSILI
<dead_dasia> <Greek_alpha>		: "ἁ"	U1F01 # GREEK SMALL LETTER ALPHA WITH DASIA
<Multi_key> <parenleft> <Greek_alpha>	: "ἁ"	U1F01 # GREEK SMALL LETTER ALPHA WITH DASIA
<dead_grave> <dead_psili> <Greek_alpha>	: "ἂ"	U1F02 # GREEK SMALL LETTER ALPHA WITH PSILI AND VARIA
<dead_grave> <Multi_key> <parenright> <Greek_alpha>	: "ἂ"	U1F02 # GREEK SMALL LETTER ALPHA WITH PSILI AND VARIA
<Multi_key> <grave> <dead_psili> <Greek_alpha>	: "ἂ"	U1F02 # GREEK SMALL LETTER ALPHA WITH PSILI AND VARIA
<Multi_key> <grave> <parenright> <Greek_alpha>	: "ἂ"	U1F02 # GREEK SMALL LETTER ALPHA WITH PSILI AND VARIA
<dead_grave> <dead_dasia> <Greek_alpha>	: "ἃ"	U1F03 # GREEK SMALL LETTER ALPHA WITH DASIA AND VARIA
<dead_grave> <Multi_key> <parenleft> <Greek_alpha>	: "ἃ"	U1F03 # GREEK SMALL LETTER ALPHA WITH DASIA AND VARIA
<Multi_key> <grave> <dead_dasia> <Greek_alpha>	: "ἃ"	U1F03 # GREEK SMALL LETTER ALPHA WITH DASIA AND VARIA
<Multi_key> <grave> <parenleft> <Greek_alpha>	: "ἃ"	U1F03 # GREEK SMALL LETTER ALPHA WITH DASIA AND VARIA
<dead_acute> <dead_psili> <Greek_alpha>	: "ἄ"	U1F04 # GREEK SMALL LETTER ALPHA WITH PSILI AND OXIA
<dead_acute> <Multi_key> <parenright> <Greek_alpha>	: "ἄ"	U1F04 # GREEK SMALL LETTER ALPHA WITH PSILI AND OXIA
<Multi_key> <acute> <dead_psili> <Greek_alpha>	: "ἄ"	U1F04 # GREEK SMALL LETTER ALPHA WITH PSILI AND OXIA
<Multi_key> <acute> <parenright> <Greek_alpha>	: "ἄ"	U1F04 # GREEK SMALL LETTER ALPHA WITH PSILI AND OXIA
<Multi_key> <apostrophe> <dead_psili> <Greek_alpha>	: "ἄ"	U1F04 # GREEK SMALL LETTER ALPHA WITH PSILI AND OXIA
<Multi_key> <apostrophe> <parenright> <Greek_alpha>	: "ἄ"	U1F04 # GREEK SMALL LETTER ALPHA WITH PSILI AND OXIA
<dead_acute> <dead_dasia> <Greek_alpha>	: "ἅ"	U1F05 # GREEK SMALL LETTER ALPHA WITH DASIA AND OXIA
<dead_acute> <Multi_key> <parenleft> <Greek_alpha>	: "ἅ"	U1F05 # GREEK SMALL LETTER ALPHA WITH DASIA AND OXIA
<Multi_key> <acute> <dead_dasia> <Greek_alpha>	: "ἅ"	U1F05 # GREEK SMALL LETTER ALPHA WITH DASIA AND OXIA
<Multi_key> <acute> <parenleft> <Greek_alpha>	: "ἅ"	U1F05 # GREEK SMALL LETTER ALPHA WITH DASIA AND OXIA
<Multi_key> <apostrophe> <dead_dasia> <Greek_alpha>	: "ἅ"	U1F05 # GREEK SMALL LETTER ALPHA WITH DASIA AND OXIA
<Multi_key> <apostrophe> <parenleft> <Greek_alpha>	: "ἅ"	U1F05 # GREEK SMALL LETTER ALPHA WITH DASIA AND OXIA
<dead_tilde> <dead_psili> <Greek_alpha>	: "ἆ"	U1F06 # GREEK SMALL LETTER ALPHA WITH PSILI AND PERISPOMENI
<dead_tilde> <Multi_key> <parenright> <Greek_alpha>	: "ἆ"	U1F06 # GREEK SMALL LETTER ALPHA WITH PSILI AND PERISPOMENI
<Multi_key> <asciitilde> <dead_psili> <Greek_alpha>	: "ἆ"	U1F06 # GREEK SMALL LETTER ALPHA WITH PSILI AND PERISPOMENI
<Multi_key> <asciitilde> <parenright> <Greek_alpha>	: "ἆ"	U1F06 # GREEK SMALL LETTER ALPHA WITH PSILI AND PERISPOMENI
<dead_tilde> <dead_dasia> <Greek_alpha>	: "ἇ"	U1F07 # GREEK SMALL LETTER ALPHA WITH DASIA AND PERISPOMENI
<dead_tilde> <Multi_key> <parenleft> <Greek_alpha>	: "ἇ"	U1F07 # GREEK SMALL LETTER ALPHA WITH DASIA AND PERISPOMENI
<Multi_key> <asciitilde> <dead_dasia> <Greek_alpha>	: "ἇ"	U1F07 # GREEK SMALL LETTER ALPHA WITH DASIA AND PERISPOMENI
<Multi_key> <asciitilde> <parenleft> <Greek_alpha>	: "ἇ"	U1F07 # GREEK SMALL LETTER ALPHA WITH DASIA AND PERISPOMENI
<dead_psili> <Greek_ALPHA>		: "Ἀ"	U1F08 # GREEK CAPITAL LETTER ALPHA WITH PSILI
<Multi_key> <parenright> <Greek_ALPHA>	: "Ἀ"	U1F08 # GREEK CAPITAL LETTER ALPHA WITH PSILI
<dead_dasia> <Greek_ALPHA>		: "Ἁ"	U1F09 # GREEK CAPITAL LETTER ALPHA WITH DASIA
<Multi_key> <parenleft> <Greek_ALPHA>	: "Ἁ"	U1F09 # GREEK CAPITAL LETTER ALPHA WITH DASIA
<dead_grave> <dead_psili> <Greek_ALPHA>	: "Ἂ"	U1F0A # GREEK CAPITAL LETTER ALPHA WITH PSILI AND VARIA
<dead_grave> <Multi_key> <parenright> <Greek_ALPHA>	: "Ἂ"	U1F0A # GREEK CAPITAL LETTER ALPHA WITH PSILI AND VARIA
<Multi_key> <grave> <dead_psili> <Greek_ALPHA>	: "Ἂ"	U1F0A # GREEK CAPITAL LETTER ALPHA WITH PSILI AND VARIA
<Multi_key> <grave> <parenright> <Greek_ALPHA>	: "Ἂ"	U1F0A # GREEK CAPITAL LETTER ALPHA WITH PSILI AND VARIA
<dead_grave> <dead_dasia> <Greek_ALPHA>	: "Ἃ"	U1F0B # GREEK CAPITAL LETTER ALPHA WITH DASIA AND VARIA
<dead_grave> <Multi_key> <parenleft> <Greek_ALPHA>	: "Ἃ"	U1F0B # GREEK CAPITAL LETTER ALPHA WITH DASIA AND VARIA
<Multi_key> <grave> <dead_dasia> <Greek_ALPHA>	: "Ἃ"	U1F0B # GREEK CAPITAL LETTER ALPHA WITH DASIA AND VARIA
<Multi_key> <grave> <parenleft> <Greek_ALPHA>	: "Ἃ"	U1F0B # GREEK CAPITAL LETTER ALPHA WITH DASIA AND VARIA
<dead_acute> <dead_psili> <Greek_ALPHA>	: "Ἄ"	U1F0C # GREEK CAPITAL LETTER ALPHA WITH PSILI AND OXIA
<dead_acute> <Multi_key> <parenright> <Greek_ALPHA>	: "Ἄ"	U1F0C # GREEK CAPITAL LETTER ALPHA WITH PSILI AND OXIA
<Multi_key> <acute> <dead_psili> <Greek_ALPHA>	: "Ἄ"	U1F0C # GREEK CAPITAL LETTER ALPHA WITH PSILI AND OXIA
<Multi_key> <acute> <parenright> <Greek_ALPHA>	: "Ἄ"	U1F0C # GREEK CAPITAL LETTER ALPHA WITH PSILI AND OXIA
<Multi_key> <apostrophe> <dead_psili> <Greek_ALPHA>	: "Ἄ"	U1F0C # GREEK CAPITAL LETTER ALPHA WITH PSILI AND OXIA
<Multi_key> <apostrophe> <parenright> <Greek_ALPHA>	: "Ἄ"	U1F0C # GREEK CAPITAL LETTER ALPHA WITH PSILI AND OXIA
<dead_acute> <dead_dasia> <Greek_ALPHA>	: "Ἅ"	U1F0D # GREEK CAPITAL LETTER ALPHA WITH DASIA AND OXIA
<dead_acute> <Multi_key> <parenleft> <Greek_ALPHA>	: "Ἅ"	U1F0D # GREEK CAPITAL LETTER ALPHA WITH DASIA AND OXIA
<Multi_key> <acute> <dead_dasia> <Greek_ALPHA>	: "Ἅ"	U1F0D # GREEK CAPITAL LETTER ALPHA WITH DASIA AND OXIA
<Multi_key> <acute> <parenleft> <Greek_ALPHA>	: "Ἅ"	U1F0D # GREEK CAPITAL LETTER ALPHA WITH DASIA AND OXIA
<Multi_key> <apostrophe> <dead_dasia> <Greek_ALPHA>	: "Ἅ"	U1F0D # GREEK CAPITAL LETTER ALPHA WITH DASIA AND OXIA
<Multi_key> <apostrophe> <parenleft> <Greek_ALPHA>	: "Ἅ"	U1F0D # GREEK CAPITAL LETTER ALPHA WITH DASIA AND OXIA
<dead_tilde> <dead_psili> <Greek_ALPHA>	: "Ἆ"	U1F0E # GREEK CAPITAL LETTER ALPHA WITH PSILI AND PERISPOMENI
<dead_tilde> <Multi_key> <parenright> <Greek_ALPHA>	: "Ἆ"	U1F0E # GREEK CAPITAL LETTER ALPHA WITH PSILI AND PERISPOMENI
<Multi_key> <asciitilde> <dead_psili> <Greek_ALPHA>	: "Ἆ"	U1F0E # GREEK CAPITAL LETTER ALPHA WITH PSILI AND PERISPOMENI
<Multi_key> <asciitilde> <parenright> <Greek_ALPHA>	: "Ἆ"	U1F0E # GREEK CAPITAL LETTER ALPHA WITH PSILI AND PERISPOMENI
<dead_tilde> <dead_dasia> <Greek_ALPHA>	: "Ἇ"	U1F0F # GREEK CAPITAL LETTER ALPHA WITH DASIA AND PERISPOMENI
<dead_tilde> <Multi_key> <parenleft> <Greek_ALPHA>	: "Ἇ"	U1F0F # GREEK CAPITAL LETTER ALPHA WITH DASIA AND PERISPOMENI
<Multi_key> <asciitilde> <dead_dasia> <Greek_ALPHA>	: "Ἇ"	U1F0F # GREEK CAPITAL LETTER ALPHA WITH DASIA AND PERISPOMENI
<Multi_key> <asciitilde> <parenleft> <Greek_ALPHA>	: "Ἇ"	U1F0F # GREEK CAPITAL LETTER ALPHA WITH DASIA AND PERISPOMENI
<dead_psili> <Greek_epsilon>		: "ἐ"	U1F10 # GREEK SMALL LETTER EPSILON WITH PSILI
<Multi_key> <parenright> <Greek_epsilon>	: "ἐ"	U1F10 # GREEK SMALL LETTER EPSILON WITH PSILI
<dead_dasia> <Greek_epsilon>		: "ἑ"	U1F11 # GREEK SMALL LETTER EPSILON WITH DASIA
<Multi_key> <parenleft> <Greek_epsilon>	: "ἑ"	U1F11 # GREEK SMALL LETTER EPSILON WITH DASIA
<dead_grave> <dead_psili> <Greek_epsilon>	: "ἒ"	U1F12 # GREEK SMALL LETTER EPSILON WITH PSILI AND VARIA
<dead_grave> <Multi_key> <parenright> <Greek_epsilon>	: "ἒ"	U1F12 # GREEK SMALL LETTER EPSILON WITH PSILI AND VARIA
<Multi_key> <grave> <dead_psili> <Greek_epsilon>	: "ἒ"	U1F12 # GREEK SMALL LETTER EPSILON WITH PSILI AND VARIA
<Multi_key> <grave> <parenright> <Greek_epsilon>	: "ἒ"	U1F12 # GREEK SMALL LETTER EPSILON WITH PSILI AND VARIA
<dead_grave> <dead_dasia> <Greek_epsilon>	: "ἓ"	U1F13 # GREEK SMALL LETTER EPSILON WITH DASIA AND VARIA
<dead_grave> <Multi_key> <parenleft> <Greek_epsilon>	: "ἓ"	U1F13 # GREEK SMALL LETTER EPSILON WITH DASIA AND VARIA
<Multi_key> <grave> <dead_dasia> <Greek_epsilon>	: "ἓ"	U1F13 # GREEK SMALL LETTER EPSILON WITH DASIA AND VARIA
<Multi_key> <grave> <parenleft> <Greek_epsilon>	: "ἓ"	U1F13 # GREEK SMALL LETTER EPSILON WITH DASIA AND VARIA
<dead_acute> <dead_psili> <Greek_epsilon>	: "ἔ"	U1F14 # GREEK SMALL LETTER EPSILON WITH PSILI AND OXIA
<dead_acute> <Multi_key> <parenright> <Greek_epsilon>	: "ἔ"	U1F14 # GREEK SMALL LETTER EPSILON WITH PSILI AND OXIA
<Multi_key> <acute> <dead_psili> <Greek_epsilon>	: "ἔ"	U1F14 # GREEK SMALL LETTER EPSILON WITH PSILI AND OXIA
<Multi_key> <acute> <parenright> <Greek_epsilon>	: "ἔ"	U1F14 # GREEK SMALL LETTER EPSILON WITH PSILI AND OXIA
<Multi_key> <apostrophe> <dead_psili> <Greek_epsilon>	: "ἔ"	U1F14 # GREEK SMALL LETTER EPSILON WITH PSILI AND OXIA
<Multi_key> <apostrophe> <parenright> <Greek_epsilon>	: "ἔ"	U1F14 # GREEK SMALL LETTER EPSILON WITH PSILI AND OXIA
<dead_acute> <dead_dasia> <Greek_epsilon>	: "ἕ"	U1F15 # GREEK SMALL LETTER EPSILON WITH DASIA AND OXIA
<dead_acute> <Multi_key> <parenleft> <Greek_epsilon>	: "ἕ"	U1F15 # GREEK SMALL LETTER EPSILON WITH DASIA AND OXIA
<Multi_key> <acute> <dead_dasia> <Greek_epsilon>	: "ἕ"	U1F15 # GREEK SMALL LETTER EPSILON WITH DASIA AND OXIA
<Multi_key> <acute> <parenleft> <Greek_epsilon>	: "ἕ"	U1F15 # GREEK SMALL LETTER EPSILON WITH DASIA AND OXIA
<Multi_key> <apostrophe> <dead_dasia> <Greek_epsilon>	: "ἕ"	U1F15 # GREEK SMALL LETTER EPSILON WITH DASIA AND OXIA
<Multi_key> <apostrophe> <parenleft> <Greek_epsilon>	: "ἕ"	U1F15 # GREEK SMALL LETTER EPSILON WITH DASIA AND OXIA
<dead_psili> <Greek_EPSILON>		: "Ἐ"	U1F18 # GREEK CAPITAL LETTER EPSILON WITH PSILI
<Multi_key> <parenright> <Greek_EPSILON>	: "Ἐ"	U1F18 # GREEK CAPITAL LETTER EPSILON WITH PSILI
<dead_dasia> <Greek_EPSILON>		: "Ἑ"	U1F19 # GREEK CAPITAL LETTER EPSILON WITH DASIA
<Multi_key> <parenleft> <Greek_EPSILON>	: "Ἑ"	U1F19 # GREEK CAPITAL LETTER EPSILON WITH DASIA
<dead_grave> <dead_psili> <Greek_EPSILON>	: "Ἒ"	U1F1A # GREEK CAPITAL LETTER EPSILON WITH PSILI AND VARIA
<dead_grave> <Multi_key> <parenright> <Greek_EPSILON>	: "Ἒ"	U1F1A # GREEK CAPITAL LETTER EPSILON WITH PSILI AND VARIA
<Multi_key> <grave> <dead_psili> <Greek_EPSILON>	: "Ἒ"	U1F1A # GREEK CAPITAL LETTER EPSILON WITH PSILI AND VARIA
<Multi_key> <grave> <parenright> <Greek_EPSILON>	: "Ἒ"	U1F1A # GREEK CAPITAL LETTER EPSILON WITH PSILI AND VARIA
<dead_grave> <dead_dasia> <Greek_EPSILON>	: "Ἓ"	U1F1B # GREEK CAPITAL LETTER EPSILON WITH DASIA AND VARIA
<dead_grave> <Multi_key> <parenleft> <Greek_EPSILON>	: "Ἓ"	U1F1B # GREEK CAPITAL LETTER EPSILON WITH DASIA AND VARIA
<Multi_key> <grave> <dead_dasia> <Greek_EPSILON>	: "Ἓ"	U1F1B # GREEK CAPITAL LETTER EPSILON WITH DASIA AND VARIA
<Multi_key> <grave> <parenleft> <Greek_EPSILON>	: "Ἓ"	U1F1B # GREEK CAPITAL LETTER EPSILON WITH DASIA AND VARIA
<dead_acute> <dead_psili> <Greek_EPSILON>	: "Ἔ"	U1F1C # GREEK CAPITAL LETTER EPSILON WITH PSILI AND OXIA
<dead_acute> <Multi_key> <parenright> <Greek_EPSILON>	: "Ἔ"	U1F1C # GREEK CAPITAL LETTER EPSILON WITH PSILI AND OXIA
<Multi_key> <acute> <dead_psili> <Greek_EPSILON>	: "Ἔ"	U1F1C # GREEK CAPITAL LETTER EPSILON WITH PSILI AND OXIA
<Multi_key> <acute> <parenright> <Greek_EPSILON>	: "Ἔ"	U1F1C # GREEK CAPITAL LETTER EPSILON WITH PSILI AND OXIA
<Multi_key> <apostrophe> <dead_psili> <Greek_EPSILON>	: "Ἔ"	U1F1C # GREEK CAPITAL LETTER EPSILON WITH PSILI AND OXIA
<Multi_key> <apostrophe> <parenright> <Greek_EPSILON>	: "Ἔ"	U1F1C # GREEK CAPITAL LETTER EPSILON WITH PSILI AND OXIA
<dead_acute> <dead_dasia> <Greek_EPSILON>	: "Ἕ"	U1F1D # GREEK CAPITAL LETTER EPSILON WITH DASIA AND OXIA
<dead_acute> <Multi_key> <parenleft> <Greek_EPSILON>	: "Ἕ"	U1F1D # GREEK CAPITAL LETTER EPSILON WITH DASIA AND OXIA
<Multi_key> <acute> <dead_dasia> <Greek_EPSILON>	: "Ἕ"	U1F1D # GREEK CAPITAL LETTER EPSILON WITH DASIA AND OXIA
<Multi_key> <acute> <parenleft> <Greek_EPSILON>	: "Ἕ"	U1F1D # GREEK CAPITAL LETTER EPSILON WITH DASIA AND OXIA
<Multi_key> <apostrophe> <dead_dasia> <Greek_EPSILON>	: "Ἕ"	U1F1D # GREEK CAPITAL LETTER EPSILON WITH DASIA AND OXIA
<Multi_key> <apostrophe> <parenleft> <Greek_EPSILON>	: "Ἕ"	U1F1D # GREEK CAPITAL LETTER EPSILON WITH DASIA AND OXIA
<dead_psili> <Greek_eta>		: "ἠ"	U1F20 # GREEK SMALL LETTER ETA WITH PSILI
<Multi_key> <parenright> <Greek_eta>	: "ἠ"	U1F20 # GREEK SMALL LETTER ETA WITH PSILI
<dead_dasia> <Greek_eta>		: "ἡ"	U1F21 # GREEK SMALL LETTER ETA WITH DASIA
<Multi_key> <parenleft> <Greek_eta>	: "ἡ"	U1F21 # GREEK SMALL LETTER ETA WITH DASIA
<dead_grave> <dead_psili> <Greek_eta>	: "ἢ"	U1F22 # GREEK SMALL LETTER ETA WITH PSILI AND VARIA
<dead_grave> <Multi_key> <parenright> <Greek_eta>	: "ἢ"	U1F22 # GREEK SMALL LETTER ETA WITH PSILI AND VARIA
<Multi_key> <grave> <dead_psili> <Greek_eta>	: "ἢ"	U1F22 # GREEK SMALL LETTER ETA WITH PSILI AND VARIA
<Multi_key> <grave> <parenright> <Greek_eta>	: "ἢ"	U1F22 # GREEK SMALL LETTER ETA WITH PSILI AND VARIA
<dead_grave> <dead_dasia> <Greek_eta>	: "ἣ"	U1F23 # GREEK SMALL LETTER ETA WITH DASIA AND VARIA
<dead_grave> <Multi_key> <parenleft> <Greek_eta>	: "ἣ"	U1F23 # GREEK SMALL LETTER ETA WITH DASIA AND VARIA
<Multi_key> <grave> <dead_dasia> <Greek_eta>	: "ἣ"	U1F23 # GREEK SMALL LETTER ETA WITH DASIA AND VARIA
<Multi_key> <grave> <parenleft> <Greek_eta>	: "ἣ"	U1F23 # GREEK SMALL LETTER ETA WITH DASIA AND VARIA
<dead_acute> <dead_psili> <Greek_eta>	: "ἤ"	U1F24 # GREEK SMALL LETTER ETA WITH PSILI AND OXIA
<dead_acute> <Multi_key> <parenright> <Greek_eta>	: "ἤ"	U1F24 # GREEK SMALL LETTER ETA WITH PSILI AND OXIA
<Multi_key> <acute> <dead_psili> <Greek_eta>	: "ἤ"	U1F24 # GREEK SMALL LETTER ETA WITH PSILI AND OXIA
<Multi_key> <acute> <parenright> <Greek_eta>	: "ἤ"	U1F24 # GREEK SMALL LETTER ETA WITH PSILI AND OXIA
<Multi_key> <apostrophe> <dead_psili> <Greek_eta>	: "ἤ"	U1F24 # GREEK SMALL LETTER ETA WITH PSILI AND OXIA
<Multi_key> <apostrophe> <parenright> <Greek_eta>	: "ἤ"	U1F24 # GREEK SMALL LETTER ETA WITH PSILI AND OXIA
<dead_acute> <dead_dasia> <Greek_eta>	: "ἥ"	U1F25 # GREEK SMALL LETTER ETA WITH DASIA AND OXIA
<dead_acute> <Multi_key> <parenleft> <Greek_eta>	: "ἥ"	U1F25 # GREEK SMALL LETTER ETA WITH DASIA AND OXIA
<Multi_key> <acute> <dead_dasia> <Greek_eta>	: "ἥ"	U1F25 # GREEK SMALL LETTER ETA WITH DASIA AND OXIA
<Multi_key> <acute> <parenleft> <Greek_eta>	: "ἥ"	U1F25 # GREEK SMALL LETTER ETA WITH DASIA AND OXIA
<Multi_key> <apostrophe> <dead_dasia> <Greek_eta>	: "ἥ"	U1F25 # GREEK SMALL LETTER ETA WITH DASIA AND OXIA
<Multi_key> <apostrophe> <parenleft> <Greek_eta>	: "ἥ"	U1F25 # GREEK SMALL LETTER ETA WITH DASIA AND OXIA
<dead_tilde> <dead_psili> <Greek_eta>	: "ἦ"	U1F26 # GREEK SMALL LETTER ETA WITH PSILI AND PERISPOMENI
<dead_tilde> <Multi_key> <parenright> <Greek_eta>	: "ἦ"	U1F26 # GREEK SMALL LETTER ETA WITH PSILI AND PERISPOMENI
<Multi_key> <asciitilde> <dead_psili> <Greek_eta>	: "ἦ"	U1F26 # GREEK SMALL LETTER ETA WITH PSILI AND PERISPOMENI
<Multi_key> <asciitilde> <parenright> <Greek_eta>	: "ἦ"	U1F26 # GREEK SMALL LETTER ETA WITH PSILI AND PERISPOMENI
<dead_tilde> <dead_dasia> <Greek_eta>	: "ἧ"	U1F27 # GREEK SMALL LETTER ETA WITH DASIA AND PERISPOMENI
<dead_tilde> <Multi_key> <parenleft> <Greek_eta>	: "ἧ"	U1F27 # GREEK SMALL LETTER ETA WITH DASIA AND PERISPOMENI
<Multi_key> <asciitilde> <dead_dasia> <Greek_eta>	: "ἧ"	U1F27 # GREEK SMALL LETTER ETA WITH DASIA AND PERISPOMENI
<Multi_key> <asciitilde> <parenleft> <Greek_eta>	: "ἧ"	U1F27 # GREEK SMALL LETTER ETA WITH DASIA AND PERISPOMENI
<dead_psili> <Greek_ETA>		: "Ἠ"	U1F28 # GREEK CAPITAL LETTER ETA WITH PSILI
<Multi_key> <parenright> <Greek_ETA>	: "Ἠ"	U1F28 # GREEK CAPITAL LETTER ETA WITH PSILI
<dead_dasia> <Greek_ETA>		: "Ἡ"	U1F29 # GREEK CAPITAL LETTER ETA WITH DASIA
<Multi_key> <parenleft> <Greek_ETA>	: "Ἡ"	U1F29 # GREEK CAPITAL LETTER ETA WITH DASIA
<dead_grave> <dead_psili> <Greek_ETA>	: "Ἢ"	U1F2A # GREEK CAPITAL LETTER ETA WITH PSILI AND VARIA
<dead_grave> <Multi_key> <parenright> <Greek_ETA>	: "Ἢ"	U1F2A # GREEK CAPITAL LETTER ETA WITH PSILI AND VARIA
<Multi_key> <grave> <dead_psili> <Greek_ETA>	: "Ἢ"	U1F2A # GREEK CAPITAL LETTER ETA WITH PSILI AND VARIA
<Multi_key> <grave> <parenright> <Greek_ETA>	: "Ἢ"	U1F2A # GREEK CAPITAL LETTER ETA WITH PSILI AND VARIA
<dead_grave> <dead_dasia> <Greek_ETA>	: "Ἣ"	U1F2B # GREEK CAPITAL LETTER ETA WITH DASIA AND VARIA
<dead_grave> <Multi_key> <parenleft> <Greek_ETA>	: "Ἣ"	U1F2B # GREEK CAPITAL LETTER ETA WITH DASIA AND VARIA
<Multi_key> <grave> <dead_dasia> <Greek_ETA>	: "Ἣ"	U1F2B # GREEK CAPITAL LETTER ETA WITH DASIA AND VARIA
<Multi_key> <grave> <parenleft> <Greek_ETA>	: "Ἣ"	U1F2B # GREEK CAPITAL LETTER ETA WITH DASIA AND VARIA
<dead_acute> <dead_psili> <Greek_ETA>	: "Ἤ"	U1F2C # GREEK CAPITAL LETTER ETA WITH PSILI AND OXIA
<dead_acute> <Multi_key> <parenright> <Greek_ETA>	: "Ἤ"	U1F2C # GREEK CAPITAL LETTER ETA WITH PSILI AND OXIA
<Multi_key> <acute> <dead_psili> <Greek_ETA>	: "Ἤ"	U1F2C # GREEK CAPITAL LETTER ETA WITH PSILI AND OXIA
<Multi_key> <acute> <parenright> <Greek_ETA>	: "Ἤ"	U1F2C # GREEK CAPITAL LETTER ETA WITH PSILI AND OXIA
<Multi_key> <apostrophe> <dead_psili> <Greek_ETA>	: "Ἤ"	U1F2C # GREEK CAPITAL LETTER ETA WITH PSILI AND OXIA
<Multi_key> <apostrophe> <parenright> <Greek_ETA>	: "Ἤ"	U1F2C # GREEK CAPITAL LETTER ETA WITH PSILI AND OXIA
<dead_acute> <dead_dasia> <Greek_ETA>	: "Ἥ"	U1F2D # GREEK CAPITAL LETTER ETA WITH DASIA AND OXIA
<dead_acute> <Multi_key> <parenleft> <Greek_ETA>	: "Ἥ"	U1F2D # GREEK CAPITAL LETTER ETA WITH DASIA AND OXIA
<Multi_key> <acute> <dead_dasia> <Greek_ETA>	: "Ἥ"	U1F2D # GREEK CAPITAL LETTER ETA WITH DASIA AND OXIA
<Multi_key> <acute> <parenleft> <Greek_ETA>	: "Ἥ"	U1F2D # GREEK CAPITAL LETTER ETA WITH DASIA AND OXIA
<Multi_key> <apostrophe> <dead_dasia> <Greek_ETA>	: "Ἥ"	U1F2D # GREEK CAPITAL LETTER ETA WITH DASIA AND OXIA
<Multi_key> <apostrophe> <parenleft> <Greek_ETA>	: "Ἥ"	U1F2D # GREEK CAPITAL LETTER ETA WITH DASIA AND OXIA
<dead_tilde> <dead_psili> <Greek_ETA>	: "Ἦ"	U1F2E # GREEK CAPITAL LETTER ETA WITH PSILI AND PERISPOMENI
<dead_tilde> <Multi_key> <parenright> <Greek_ETA>	: "Ἦ"	U1F2E # GREEK CAPITAL LETTER ETA WITH PSILI AND PERISPOMENI
<Multi_key> <asciitilde> <dead_psili> <Greek_ETA>	: "Ἦ"	U1F2E # GREEK CAPITAL LETTER ETA WITH PSILI AND PERISPOMENI
<Multi_key> <asciitilde> <parenright> <Greek_ETA>	: "Ἦ"	U1F2E # GREEK CAPITAL LETTER ETA WITH PSILI AND PERISPOMENI
<dead_tilde> <dead_dasia> <Greek_ETA>	: "Ἧ"	U1F2F # GREEK CAPITAL LETTER ETA WITH DASIA AND PERISPOMENI
<dead_tilde> <Multi_key> <parenleft> <Greek_ETA>	: "Ἧ"	U1F2F # GREEK CAPITAL LETTER ETA WITH DASIA AND PERISPOMENI
<Multi_key> <asciitilde> <dead_dasia> <Greek_ETA>	: "Ἧ"	U1F2F # GREEK CAPITAL LETTER ETA WITH DASIA AND PERISPOMENI
<Multi_key> <asciitilde> <parenleft> <Greek_ETA>	: "Ἧ"	U1F2F # GREEK CAPITAL LETTER ETA WITH DASIA AND PERISPOMENI
<dead_psili> <Greek_iota>		: "ἰ"	U1F30 # GREEK SMALL LETTER IOTA WITH PSILI
<Multi_key> <parenright> <Greek_iota>	: "ἰ"	U1F30 # GREEK SMALL LETTER IOTA WITH PSILI
<dead_dasia> <Greek_iota>		: "ἱ"	U1F31 # GREEK SMALL LETTER IOTA WITH DASIA
<Multi_key> <parenleft> <Greek_iota>	: "ἱ"	U1F31 # GREEK SMALL LETTER IOTA WITH DASIA
<dead_grave> <dead_psili> <Greek_iota>	: "ἲ"	U1F32 # GREEK SMALL LETTER IOTA WITH PSILI AND VARIA
<dead_grave> <Multi_key> <parenright> <Greek_iota>	: "ἲ"	U1F32 # GREEK SMALL LETTER IOTA WITH PSILI AND VARIA
<Multi_key> <grave> <dead_psili> <Greek_iota>	: "ἲ"	U1F32 # GREEK SMALL LETTER IOTA WITH PSILI AND VARIA
<Multi_key> <grave> <parenright> <Greek_iota>	: "ἲ"	U1F32 # GREEK SMALL LETTER IOTA WITH PSILI AND VARIA
<dead_grave> <dead_dasia> <Greek_iota>	: "ἳ"	U1F33 # GREEK SMALL LETTER IOTA WITH DASIA AND VARIA
<dead_grave> <Multi_key> <parenleft> <Greek_iota>	: "ἳ"	U1F33 # GREEK SMALL LETTER IOTA WITH DASIA AND VARIA
<Multi_key> <grave> <dead_dasia> <Greek_iota>	: "ἳ"	U1F33 # GREEK SMALL LETTER IOTA WITH DASIA AND VARIA
<Multi_key> <grave> <parenleft> <Greek_iota>	: "ἳ"	U1F33 # GREEK SMALL LETTER IOTA WITH DASIA AND VARIA
<dead_acute> <dead_psili> <Greek_iota>	: "ἴ"	U1F34 # GREEK SMALL LETTER IOTA WITH PSILI AND OXIA
<dead_acute> <Multi_key> <parenright> <Greek_iota>	: "ἴ"	U1F34 # GREEK SMALL LETTER IOTA WITH PSILI AND OXIA
<Multi_key> <acute> <dead_psili> <Greek_iota>	: "ἴ"	U1F34 # GREEK SMALL LETTER IOTA WITH PSILI AND OXIA
<Multi_key> <acute> <parenright> <Greek_iota>	: "ἴ"	U1F34 # GREEK SMALL LETTER IOTA WITH PSILI AND OXIA
<Multi_key> <apostrophe> <dead_psili> <Greek_iota>	: "ἴ"	U1F34 # GREEK SMALL LETTER IOTA WITH PSILI AND OXIA
<Multi_key> <apostrophe> <parenright> <Greek_iota>	: "ἴ"	U1F34 # GREEK SMALL LETTER IOTA WITH PSILI AND OXIA
<dead_acute> <dead_dasia> <Greek_iota>	: "ἵ"	U1F35 # GREEK SMALL LETTER IOTA WITH DASIA AND OXIA
<dead_acute> <Multi_key> <parenleft> <Greek_iota>	: "ἵ"	U1F35 # GREEK SMALL LETTER IOTA WITH DASIA AND OXIA
<Multi_key> <acute> <dead_dasia> <Greek_iota>	: "ἵ"	U1F35 # GREEK SMALL LETTER IOTA WITH DASIA AND OXIA
<Multi_key> <acute> <parenleft> <Greek_iota>	: "ἵ"	U1F35 # GREEK SMALL LETTER IOTA WITH DASIA AND OXIA
<Multi_key> <apostrophe> <dead_dasia> <Greek_iota>	: "ἵ"	U1F35 # GREEK SMALL LETTER IOTA WITH DASIA AND OXIA
<Multi_key> <apostrophe> <parenleft> <Greek_iota>	: "ἵ"	U1F35 # GREEK SMALL LETTER IOTA WITH DASIA AND OXIA
<dead_tilde> <dead_psili> <Greek_iota>	: "ἶ"	U1F36 # GREEK SMALL LETTER IOTA WITH PSILI AND PERISPOMENI
<dead_tilde> <Multi_key> <parenright> <Greek_iota>	: "ἶ"	U1F36 # GREEK SMALL LETTER IOTA WITH PSILI AND PERISPOMENI
<Multi_key> <asciitilde> <dead_psili> <Greek_iota>	: "ἶ"	U1F36 # GREEK SMALL LETTER IOTA WITH PSILI AND PERISPOMENI
<Multi_key> <asciitilde> <parenright> <Greek_iota>	: "ἶ"	U1F36 # GREEK SMALL LETTER IOTA WITH PSILI AND PERISPOMENI
<dead_tilde> <dead_dasia> <Greek_iota>	: "ἷ"	U1F37 # GREEK SMALL LETTER IOTA WITH DASIA AND PERISPOMENI
<dead_tilde> <Multi_key> <parenleft> <Greek_iota>	: "ἷ"	U1F37 # GREEK SMALL LETTER IOTA WITH DASIA AND PERISPOMENI
<Multi_key> <asciitilde> <dead_dasia> <Greek_iota>	: "ἷ"	U1F37 # GREEK SMALL LETTER IOTA WITH DASIA AND PERISPOMENI
<Multi_key> <asciitilde> <parenleft> <Greek_iota>	: "ἷ"	U1F37 # GREEK SMALL LETTER IOTA WITH DASIA AND PERISPOMENI
<dead_psili> <Greek_IOTA>		: "Ἰ"	U1F38 # GREEK CAPITAL LETTER IOTA WITH PSILI
<Multi_key> <parenright> <Greek_IOTA>	: "Ἰ"	U1F38 # GREEK CAPITAL LETTER IOTA WITH PSILI
<dead_dasia> <Greek_IOTA>		: "Ἱ"	U1F39 # GREEK CAPITAL LETTER IOTA WITH DASIA
<Multi_key> <parenleft> <Greek_IOTA>	: "Ἱ"	U1F39 # GREEK CAPITAL LETTER IOTA WITH DASIA
<dead_grave> <dead_psili> <Greek_IOTA>	: "Ἲ"	U1F3A # GREEK CAPITAL LETTER IOTA WITH PSILI AND VARIA
<dead_grave> <Multi_key> <parenright> <Greek_IOTA>	: "Ἲ"	U1F3A # GREEK CAPITAL LETTER IOTA WITH PSILI AND VARIA
<Multi_key> <grave> <dead_psili> <Greek_IOTA>	: "Ἲ"	U1F3A # GREEK CAPITAL LETTER IOTA WITH PSILI AND VARIA
<Multi_key> <grave> <parenright> <Greek_IOTA>	: "Ἲ"	U1F3A # GREEK CAPITAL LETTER IOTA WITH PSILI AND VARIA
<dead_grave> <dead_dasia> <Greek_IOTA>	: "Ἳ"	U1F3B # GREEK CAPITAL LETTER IOTA WITH DASIA AND VARIA
<dead_grave> <Multi_key> <parenleft> <Greek_IOTA>	: "Ἳ"	U1F3B # GREEK CAPITAL LETTER IOTA WITH DASIA AND VARIA
<Multi_key> <grave> <dead_dasia> <Greek_IOTA>	: "Ἳ"	U1F3B # GREEK CAPITAL LETTER IOTA WITH DASIA AND VARIA
<Multi_key> <grave> <parenleft> <Greek_IOTA>	: "Ἳ"	U1F3B # GREEK CAPITAL LETTER IOTA WITH DASIA AND VARIA
<dead_acute> <dead_psili> <Greek_IOTA>	: "Ἴ"	U1F3C # GREEK CAPITAL LETTER IOTA WITH PSILI AND OXIA
<dead_acute> <Multi_key> <parenright> <Greek_IOTA>	: "Ἴ"	U1F3C # GREEK CAPITAL LETTER IOTA WITH PSILI AND OXIA
<Multi_key> <acute> <dead_psili> <Greek_IOTA>	: "Ἴ"	U1F3C # GREEK CAPITAL LETTER IOTA WITH PSILI AND OXIA
<Multi_key> <acute> <parenright> <Greek_IOTA>	: "Ἴ"	U1F3C # GREEK CAPITAL LETTER IOTA WITH PSILI AND OXIA
<Multi_key> <apostrophe> <dead_psili> <Greek_IOTA>	: "Ἴ"	U1F3C # GREEK CAPITAL LETTER IOTA WITH PSILI AND OXIA
<Multi_key> <apostrophe> <parenright> <Greek_IOTA>	: "Ἴ"	U1F3C # GREEK CAPITAL LETTER IOTA WITH PSILI AND OXIA
<dead_acute> <dead_dasia> <Greek_IOTA>	: "Ἵ"	U1F3D # GREEK CAPITAL LETTER IOTA WITH DASIA AND OXIA
<dead_acute> <Multi_key> <parenleft> <Greek_IOTA>	: "Ἵ"	U1F3D # GREEK CAPITAL LETTER IOTA WITH DASIA AND OXIA
<Multi_key> <acute> <dead_dasia> <Greek_IOTA>	: "Ἵ"	U1F3D # GREEK CAPITAL LETTER IOTA WITH DASIA AND OXIA
<Multi_key> <acute> <parenleft> <Greek_IOTA>	: "Ἵ"	U1F3D # GREEK CAPITAL LETTER IOTA WITH DASIA AND OXIA
<Multi_key> <apostrophe> <dead_dasia> <Greek_IOTA>	: "Ἵ"	U1F3D # GREEK CAPITAL LETTER IOTA WITH DASIA AND OXIA
<Multi_key> <apostrophe> <parenleft> <Greek_IOTA>	: "Ἵ"	U1F3D # GREEK CAPITAL LETTER IOTA WITH DASIA AND OXIA
<dead_tilde> <dead_psili> <Greek_IOTA>	: "Ἶ"	U1F3E # GREEK CAPITAL LETTER IOTA WITH PSILI AND PERISPOMENI
<dead_tilde> <Multi_key> <parenright> <Greek_IOTA>	: "Ἶ"	U1F3E # GREEK CAPITAL LETTER IOTA WITH PSILI AND PERISPOMENI
<Multi_key> <asciitilde> <dead_psili> <Greek_IOTA>	: "Ἶ"	U1F3E # GREEK CAPITAL LETTER IOTA WITH PSILI AND PERISPOMENI
<Multi_key> <asciitilde> <parenright> <Greek_IOTA>	: "Ἶ"	U1F3E # GREEK CAPITAL LETTER IOTA WITH PSILI AND PERISPOMENI
<dead_tilde> <dead_dasia> <Greek_IOTA>	: "Ἷ"	U1F3F # GREEK CAPITAL LETTER IOTA WITH DASIA AND PERISPOMENI
<dead_tilde> <Multi_key> <parenleft> <Greek_IOTA>	: "Ἷ"	U1F3F # GREEK CAPITAL LETTER IOTA WITH DASIA AND PERISPOMENI
<Multi_key> <asciitilde> <dead_dasia> <Greek_IOTA>	: "Ἷ"	U1F3F # GREEK CAPITAL LETTER IOTA WITH DASIA AND PERISPOMENI
<Multi_key> <asciitilde> <parenleft> <Greek_IOTA>	: "Ἷ"	U1F3F # GREEK CAPITAL LETTER IOTA WITH DASIA AND PERISPOMENI
<dead_psili> <Greek_omicron>		: "ὀ"	U1F40 # GREEK SMALL LETTER OMICRON WITH PSILI
<Multi_key> <parenright> <Greek_omicron>	: "ὀ"	U1F40 # GREEK SMALL LETTER OMICRON WITH PSILI
<dead_dasia> <Greek_omicron>		: "ὁ"	U1F41 # GREEK SMALL LETTER OMICRON WITH DASIA
<Multi_key> <parenleft> <Greek_omicron>	: "ὁ"	U1F41 # GREEK SMALL LETTER OMICRON WITH DASIA
<dead_grave> <dead_psili> <Greek_omicron>	: "ὂ"	U1F42 # GREEK SMALL LETTER OMICRON WITH PSILI AND VARIA
<dead_grave> <Multi_key> <parenright> <Greek_omicron>	: "ὂ"	U1F42 # GREEK SMALL LETTER OMICRON WITH PSILI AND VARIA
<Multi_key> <grave> <dead_psili> <Greek_omicron>	: "ὂ"	U1F42 # GREEK SMALL LETTER OMICRON WITH PSILI AND VARIA
<Multi_key> <grave> <parenright> <Greek_omicron>	: "ὂ"	U1F42 # GREEK SMALL LETTER OMICRON WITH PSILI AND VARIA
<dead_grave> <dead_dasia> <Greek_omicron>	: "ὃ"	U1F43 # GREEK SMALL LETTER OMICRON WITH DASIA AND VARIA
<dead_grave> <Multi_key> <parenleft> <Greek_omicron>	: "ὃ"	U1F43 # GREEK SMALL LETTER OMICRON WITH DASIA AND VARIA
<Multi_key> <grave> <dead_dasia> <Greek_omicron>	: "ὃ"	U1F43 # GREEK SMALL LETTER OMICRON WITH DASIA AND VARIA
<Multi_key> <grave> <parenleft> <Greek_omicron>	: "ὃ"	U1F43 # GREEK SMALL LETTER OMICRON WITH DASIA AND VARIA
<dead_acute> <dead_psili> <Greek_omicron>	: "ὄ"	U1F44 # GREEK SMALL LETTER OMICRON WITH PSILI AND OXIA
<dead_acute> <Multi_key> <parenright> <Greek_omicron>	: "ὄ"	U1F44 # GREEK SMALL LETTER OMICRON WITH PSILI AND OXIA
<Multi_key> <acute> <dead_psili> <Greek_omicron>	: "ὄ"	U1F44 # GREEK SMALL LETTER OMICRON WITH PSILI AND OXIA
<Multi_key> <acute> <parenright> <Greek_omicron>	: "ὄ"	U1F44 # GREEK SMALL LETTER OMICRON WITH PSILI AND OXIA
<Multi_key> <apostrophe> <dead_psili> <Greek_omicron>	: "ὄ"	U1F44 # GREEK SMALL LETTER OMICRON WITH PSILI AND OXIA
<Multi_key> <apostrophe> <parenright> <Greek_omicron>	: "ὄ"	U1F44 # GREEK SMALL LETTER OMICRON WITH PSILI AND OXIA
<dead_acute> <dead_dasia> <Greek_omicron>	: "ὅ"	U1F45 # GREEK SMALL LETTER OMICRON WITH DASIA AND OXIA
<dead_acute> <Multi_key> <parenleft> <Greek_omicron>	: "ὅ"	U1F45 # GREEK SMALL LETTER OMICRON WITH DASIA AND OXIA
<Multi_key> <acute> <dead_dasia> <Greek_omicron>	: "ὅ"	U1F45 # GREEK SMALL LETTER OMICRON WITH DASIA AND OXIA
<Multi_key> <acute> <parenleft> <Greek_omicron>	: "ὅ"	U1F45 # GREEK SMALL LETTER OMICRON WITH DASIA AND OXIA
<Multi_key> <apostrophe> <dead_dasia> <Greek_omicron>	: "ὅ"	U1F45 # GREEK SMALL LETTER OMICRON WITH DASIA AND OXIA
<Multi_key> <apostrophe> <parenleft> <Greek_omicron>	: "ὅ"	U1F45 # GREEK SMALL LETTER OMICRON WITH DASIA AND OXIA
<dead_psili> <Greek_OMICRON>		: "Ὀ"	U1F48 # GREEK CAPITAL LETTER OMICRON WITH PSILI
<Multi_key> <parenright> <Greek_OMICRON>	: "Ὀ"	U1F48 # GREEK CAPITAL LETTER OMICRON WITH PSILI
<dead_dasia> <Greek_OMICRON>		: "Ὁ"	U1F49 # GREEK CAPITAL LETTER OMICRON WITH DASIA
<Multi_key> <parenleft> <Greek_OMICRON>	: "Ὁ"	U1F49 # GREEK CAPITAL LETTER OMICRON WITH DASIA
<dead_grave> <dead_psili> <Greek_OMICRON>	: "Ὂ"	U1F4A # GREEK CAPITAL LETTER OMICRON WITH PSILI AND VARIA
<dead_grave> <Multi_key> <parenright> <Greek_OMICRON>	: "Ὂ"	U1F4A # GREEK CAPITAL LETTER OMICRON WITH PSILI AND VARIA
<Multi_key> <grave> <dead_psili> <Greek_OMICRON>	: "Ὂ"	U1F4A # GREEK CAPITAL LETTER OMICRON WITH PSILI AND VARIA
<Multi_key> <grave> <parenright> <Greek_OMICRON>	: "Ὂ"	U1F4A # GREEK CAPITAL LETTER OMICRON WITH PSILI AND VARIA
<dead_grave> <dead_dasia> <Greek_OMICRON>	: "Ὃ"	U1F4B # GREEK CAPITAL LETTER OMICRON WITH DASIA AND VARIA
<dead_grave> <Multi_key> <parenleft> <Greek_OMICRON>	: "Ὃ"	U1F4B # GREEK CAPITAL LETTER OMICRON WITH DASIA AND VARIA
<Multi_key> <grave> <dead_dasia> <Greek_OMICRON>	: "Ὃ"	U1F4B # GREEK CAPITAL LETTER OMICRON WITH DASIA AND VARIA
<Multi_key> <grave> <parenleft> <Greek_OMICRON>	: "Ὃ"	U1F4B # GREEK CAPITAL LETTER OMICRON WITH DASIA AND VARIA
<dead_acute> <dead_psili> <Greek_OMICRON>	: "Ὄ"	U1F4C # GREEK CAPITAL LETTER OMICRON WITH PSILI AND OXIA
<dead_acute> <Multi_key> <parenright> <Greek_OMICRON>	: "Ὄ"	U1F4C # GREEK CAPITAL LETTER OMICRON WITH PSILI AND OXIA
<Multi_key> <acute> <dead_psili> <Greek_OMICRON>	: "Ὄ"	U1F4C # GREEK CAPITAL LETTER OMICRON WITH PSILI AND OXIA
<Multi_key> <acute> <parenright> <Greek_OMICRON>	: "Ὄ"	U1F4C # GREEK CAPITAL LETTER OMICRON WITH PSILI AND OXIA
<Multi_key> <apostrophe> <dead_psili> <Greek_OMICRON>	: "Ὄ"	U1F4C # GREEK CAPITAL LETTER OMICRON WITH PSILI AND OXIA
<Multi_key> <apostrophe> <parenright> <Greek_OMICRON>	: "Ὄ"	U1F4C # GREEK CAPITAL LETTER OMICRON WITH PSILI AND OXIA
<dead_acute> <dead_dasia> <Greek_OMICRON>	: "Ὅ"	U1F4D # GREEK CAPITAL LETTER OMICRON WITH DASIA AND OXIA
<dead_acute> <Multi_key> <parenleft> <Greek_OMICRON>	: "Ὅ"	U1F4D # GREEK CAPITAL LETTER OMICRON WITH DASIA AND OXIA
<Multi_key> <acute> <dead_dasia> <Greek_OMICRON>	: "Ὅ"	U1F4D # GREEK CAPITAL LETTER OMICRON WITH DASIA AND OXIA
<Multi_key> <acute> <parenleft> <Greek_OMICRON>	: "Ὅ"	U1F4D # GREEK CAPITAL LETTER OMICRON WITH DASIA AND OXIA
<Multi_key> <apostrophe> <dead_dasia> <Greek_OMICRON>	: "Ὅ"	U1F4D # GREEK CAPITAL LETTER OMICRON WITH DASIA AND OXIA
<Multi_key> <apostrophe> <parenleft> <Greek_OMICRON>	: "Ὅ"	U1F4D # GREEK CAPITAL LETTER OMICRON WITH DASIA AND OXIA
<dead_psili> <Greek_upsilon>		: "ὐ"	U1F50 # GREEK SMALL LETTER UPSILON WITH PSILI
<Multi_key> <parenright> <Greek_upsilon>	: "ὐ"	U1F50 # GREEK SMALL LETTER UPSILON WITH PSILI
<dead_dasia> <Greek_upsilon>		: "ὑ"	U1F51 # GREEK SMALL LETTER UPSILON WITH DASIA
<Multi_key> <parenleft> <Greek_upsilon>	: "ὑ"	U1F51 # GREEK SMALL LETTER UPSILON WITH DASIA
<dead_grave> <dead_psili> <Greek_upsilon>	: "ὒ"	U1F52 # GREEK SMALL LETTER UPSILON WITH PSILI AND VARIA
<dead_grave> <Multi_key> <parenright> <Greek_upsilon>	: "ὒ"	U1F52 # GREEK SMALL LETTER UPSILON WITH PSILI AND VARIA
<Multi_key> <grave> <dead_psili> <Greek_upsilon>	: "ὒ"	U1F52 # GREEK SMALL LETTER UPSILON WITH PSILI AND VARIA
<Multi_key> <grave> <parenright> <Greek_upsilon>	: "ὒ"	U1F52 # GREEK SMALL LETTER UPSILON WITH PSILI AND VARIA
<dead_grave> <dead_dasia> <Greek_upsilon>	: "ὓ"	U1F53 # GREEK SMALL LETTER UPSILON WITH DASIA AND VARIA
<dead_grave> <Multi_key> <parenleft> <Greek_upsilon>	: "ὓ"	U1F53 # GREEK SMALL LETTER UPSILON WITH DASIA AND VARIA
<Multi_key> <grave> <dead_dasia> <Greek_upsilon>	: "ὓ"	U1F53 # GREEK SMALL LETTER UPSILON WITH DASIA AND VARIA
<Multi_key> <grave> <parenleft> <Greek_upsilon>	: "ὓ"	U1F53 # GREEK SMALL LETTER UPSILON WITH DASIA AND VARIA
<dead_acute> <dead_psili> <Greek_upsilon>	: "ὔ"	U1F54 # GREEK SMALL LETTER UPSILON WITH PSILI AND OXIA
<dead_acute> <Multi_key> <parenright> <Greek_upsilon>	: "ὔ"	U1F54 # GREEK SMALL LETTER UPSILON WITH PSILI AND OXIA
<Multi_key> <acute> <dead_psili> <Greek_upsilon>	: "ὔ"	U1F54 # GREEK SMALL LETTER UPSILON WITH PSILI AND OXIA
<Multi_key> <acute> <parenright> <Greek_upsilon>	: "ὔ"	U1F54 # GREEK SMALL LETTER UPSILON WITH PSILI AND OXIA
<Multi_key> <apostrophe> <dead_psili> <Greek_upsilon>	: "ὔ"	U1F54 # GREEK SMALL LETTER UPSILON WITH PSILI AND OXIA
<Multi_key> <apostrophe> <parenright> <Greek_upsilon>	: "ὔ"	U1F54 # GREEK SMALL LETTER UPSILON WITH PSILI AND OXIA
<dead_acute> <dead_dasia> <Greek_upsilon>	: "ὕ"	U1F55 # GREEK SMALL LETTER UPSILON WITH DASIA AND OXIA
<dead_acute> <Multi_key> <parenleft> <Greek_upsilon>	: "ὕ"	U1F55 # GREEK SMALL LETTER UPSILON WITH DASIA AND OXIA
<Multi_key> <acute> <dead_dasia> <Greek_upsilon>	: "ὕ"	U1F55 # GREEK SMALL LETTER UPSILON WITH DASIA AND OXIA
<Multi_key> <acute> <parenleft> <Greek_upsilon>	: "ὕ"	U1F55 # GREEK SMALL LETTER UPSILON WITH DASIA AND OXIA
<Multi_key> <apostrophe> <dead_dasia> <Greek_upsilon>	: "ὕ"	U1F55 # GREEK SMALL LETTER UPSILON WITH DASIA AND OXIA
<Multi_key> <apostrophe> <parenleft> <Greek_upsilon>	: "ὕ"	U1F55 # GREEK SMALL LETTER UPSILON WITH DASIA AND OXIA
<dead_tilde> <dead_psili> <Greek_upsilon>	: "ὖ"	U1F56 # GREEK SMALL LETTER UPSILON WITH PSILI AND PERISPOMENI
<dead_tilde> <Multi_key> <parenright> <Greek_upsilon>	: "ὖ"	U1F56 # GREEK SMALL LETTER UPSILON WITH PSILI AND PERISPOMENI
<Multi_key> <asciitilde> <dead_psili> <Greek_upsilon>	: "ὖ"	U1F56 # GREEK SMALL LETTER UPSILON WITH PSILI AND PERISPOMENI
<Multi_key> <asciitilde> <parenright> <Greek_upsilon>	: "ὖ"	U1F56 # GREEK SMALL LETTER UPSILON WITH PSILI AND PERISPOMENI
<dead_tilde> <dead_dasia> <Greek_upsilon>	: "ὗ"	U1F57 # GREEK SMALL LETTER UPSILON WITH DASIA AND PERISPOMENI
<dead_tilde> <Multi_key> <parenleft> <Greek_upsilon>	: "ὗ"	U1F57 # GREEK SMALL LETTER UPSILON WITH DASIA AND PERISPOMENI
<Multi_key> <asciitilde> <dead_dasia> <Greek_upsilon>	: "ὗ"	U1F57 # GREEK SMALL LETTER UPSILON WITH DASIA AND PERISPOMENI
<Multi_key> <asciitilde> <parenleft> <Greek_upsilon>	: "ὗ"	U1F57 # GREEK SMALL LETTER UPSILON WITH DASIA AND PERISPOMENI
<dead_dasia> <Greek_UPSILON>		: "Ὑ"	U1F59 # GREEK CAPITAL LETTER UPSILON WITH DASIA
<Multi_key> <parenleft> <Greek_UPSILON>	: "Ὑ"	U1F59 # GREEK CAPITAL LETTER UPSILON WITH DASIA
<dead_grave> <dead_dasia> <Greek_UPSILON>	: "Ὓ"	U1F5B # GREEK CAPITAL LETTER UPSILON WITH DASIA AND VARIA
<dead_grave> <Multi_key> <parenleft> <Greek_UPSILON>	: "Ὓ"	U1F5B # GREEK CAPITAL LETTER UPSILON WITH DASIA AND VARIA
<Multi_key> <grave> <dead_dasia> <Greek_UPSILON>	: "Ὓ"	U1F5B # GREEK CAPITAL LETTER UPSILON WITH DASIA AND VARIA
<Multi_key> <grave> <parenleft> <Greek_UPSILON>	: "Ὓ"	U1F5B # GREEK CAPITAL LETTER UPSILON WITH DASIA AND VARIA
<dead_acute> <dead_dasia> <Greek_UPSILON>	: "Ὕ"	U1F5D # GREEK CAPITAL LETTER UPSILON WITH DASIA AND OXIA
<dead_acute> <Multi_key> <parenleft> <Greek_UPSILON>	: "Ὕ"	U1F5D # GREEK CAPITAL LETTER UPSILON WITH DASIA AND OXIA
<Multi_key> <acute> <dead_dasia> <Greek_UPSILON>	: "Ὕ"	U1F5D # GREEK CAPITAL LETTER UPSILON WITH DASIA AND OXIA
<Multi_key> <acute> <parenleft> <Greek_UPSILON>	: "Ὕ"	U1F5D # GREEK CAPITAL LETTER UPSILON WITH DASIA AND OXIA
<Multi_key> <apostrophe> <dead_dasia> <Greek_UPSILON>	: "Ὕ"	U1F5D # GREEK CAPITAL LETTER UPSILON WITH DASIA AND OXIA
<Multi_key> <apostrophe> <parenleft> <Greek_UPSILON>	: "Ὕ"	U1F5D # GREEK CAPITAL LETTER UPSILON WITH DASIA AND OXIA
<dead_tilde> <dead_dasia> <Greek_UPSILON>	: "Ὗ"	U1F5F # GREEK CAPITAL LETTER UPSILON WITH DASIA AND PERISPOMENI
<dead_tilde> <Multi_key> <parenleft> <Greek_UPSILON>	: "Ὗ"	U1F5F # GREEK CAPITAL LETTER UPSILON WITH DASIA AND PERISPOMENI
<Multi_key> <asciitilde> <dead_dasia> <Greek_UPSILON>	: "Ὗ"	U1F5F # GREEK CAPITAL LETTER UPSILON WITH DASIA AND PERISPOMENI
<Multi_key> <asciitilde> <parenleft> <Greek_UPSILON>	: "Ὗ"	U1F5F # GREEK CAPITAL LETTER UPSILON WITH DASIA AND PERISPOMENI
<dead_psili> <Greek_omega>		: "ὠ"	U1F60 # GREEK SMALL LETTER OMEGA WITH PSILI
<Multi_key> <parenright> <Greek_omega>	: "ὠ"	U1F60 # GREEK SMALL LETTER OMEGA WITH PSILI
<dead_dasia> <Greek_omega>		: "ὡ"	U1F61 # GREEK SMALL LETTER OMEGA WITH DASIA
<Multi_key> <parenleft> <Greek_omega>	: "ὡ"	U1F61 # GREEK SMALL LETTER OMEGA WITH DASIA
<dead_grave> <dead_psili> <Greek_omega>	: "ὢ"	U1F62 # GREEK SMALL LETTER OMEGA WITH PSILI AND VARIA
<dead_grave> <Multi_key> <parenright> <Greek_omega>	: "ὢ"	U1F62 # GREEK SMALL LETTER OMEGA WITH PSILI AND VARIA
<Multi_key> <grave> <dead_psili> <Greek_omega>	: "ὢ"	U1F62 # GREEK SMALL LETTER OMEGA WITH PSILI AND VARIA
<Multi_key> <grave> <parenright> <Greek_omega>	: "ὢ"	U1F62 # GREEK SMALL LETTER OMEGA WITH PSILI AND VARIA
<dead_grave> <dead_dasia> <Greek_omega>	: "ὣ"	U1F63 # GREEK SMALL LETTER OMEGA WITH DASIA AND VARIA
<dead_grave> <Multi_key> <parenleft> <Greek_omega>	: "ὣ"	U1F63 # GREEK SMALL LETTER OMEGA WITH DASIA AND VARIA
<Multi_key> <grave> <dead_dasia> <Greek_omega>	: "ὣ"	U1F63 # GREEK SMALL LETTER OMEGA WITH DASIA AND VARIA
<Multi_key> <grave> <parenleft> <Greek_omega>	: "ὣ"	U1F63 # GREEK SMALL LETTER OMEGA WITH DASIA AND VARIA
<dead_acute> <dead_psili> <Greek_omega>	: "ὤ"	U1F64 # GREEK SMALL LETTER OMEGA WITH PSILI AND OXIA
<dead_acute> <Multi_key> <parenright> <Greek_omega>	: "ὤ"	U1F64 # GREEK SMALL LETTER OMEGA WITH PSILI AND OXIA
<Multi_key> <acute> <dead_psili> <Greek_omega>	: "ὤ"	U1F64 # GREEK SMALL LETTER OMEGA WITH PSILI AND OXIA
<Multi_key> <acute> <parenright> <Greek_omega>	: "ὤ"	U1F64 # GREEK SMALL LETTER OMEGA WITH PSILI AND OXIA
<Multi_key> <apostrophe> <dead_psili> <Greek_omega>	: "ὤ"	U1F64 # GREEK SMALL LETTER OMEGA WITH PSILI AND OXIA
<Multi_key> <apostrophe> <parenright> <Greek_omega>	: "ὤ"	U1F64 # GREEK SMALL LETTER OMEGA WITH PSILI AND OXIA
<dead_acute> <dead_dasia> <Greek_omega>	: "ὥ"	U1F65 # GREEK SMALL LETTER OMEGA WITH DASIA AND OXIA
<dead_acute> <Multi_key> <parenleft> <Greek_omega>	: "ὥ"	U1F65 # GREEK SMALL LETTER OMEGA WITH DASIA AND OXIA
<Multi_key> <acute> <dead_dasia> <Greek_omega>	: "ὥ"	U1F65 # GREEK SMALL LETTER OMEGA WITH DASIA AND OXIA
<Multi_key> <acute> <parenleft> <Greek_omega>	: "ὥ"	U1F65 # GREEK SMALL LETTER OMEGA WITH DASIA AND OXIA
<Multi_key> <apostrophe> <dead_dasia> <Greek_omega>	: "ὥ"	U1F65 # GREEK SMALL LETTER OMEGA WITH DASIA AND OXIA
<Multi_key> <apostrophe> <parenleft> <Greek_omega>	: "ὥ"	U1F65 # GREEK SMALL LETTER OMEGA WITH DASIA AND OXIA
<dead_tilde> <dead_psili> <Greek_omega>	: "ὦ"	U1F66 # GREEK SMALL LETTER OMEGA WITH PSILI AND PERISPOMENI
<dead_tilde> <Multi_key> <parenright> <Greek_omega>	: "ὦ"	U1F66 # GREEK SMALL LETTER OMEGA WITH PSILI AND PERISPOMENI
<Multi_key> <asciitilde> <dead_psili> <Greek_omega>	: "ὦ"	U1F66 # GREEK SMALL LETTER OMEGA WITH PSILI AND PERISPOMENI
<Multi_key> <asciitilde> <parenright> <Greek_omega>	: "ὦ"	U1F66 # GREEK SMALL LETTER OMEGA WITH PSILI AND PERISPOMENI
<dead_tilde> <dead_dasia> <Greek_omega>	: "ὧ"	U1F67 # GREEK SMALL LETTER OMEGA WITH DASIA AND PERISPOMENI
<dead_tilde> <Multi_key> <parenleft> <Greek_omega>	: "ὧ"	U1F67 # GREEK SMALL LETTER OMEGA WITH DASIA AND PERISPOMENI
<Multi_key> <asciitilde> <dead_dasia> <Greek_omega>	: "ὧ"	U1F67 # GREEK SMALL LETTER OMEGA WITH DASIA AND PERISPOMENI
<Multi_key> <asciitilde> <parenleft> <Greek_omega>	: "ὧ"	U1F67 # GREEK SMALL LETTER OMEGA WITH DASIA AND PERISPOMENI
<dead_psili> <Greek_OMEGA>		: "Ὠ"	U1F68 # GREEK CAPITAL LETTER OMEGA WITH PSILI
<Multi_key> <parenright> <Greek_OMEGA>	: "Ὠ"	U1F68 # GREEK CAPITAL LETTER OMEGA WITH PSILI
<dead_dasia> <Greek_OMEGA>		: "Ὡ"	U1F69 # GREEK CAPITAL LETTER OMEGA WITH DASIA
<Multi_key> <parenleft> <Greek_OMEGA>	: "Ὡ"	U1F69 # GREEK CAPITAL LETTER OMEGA WITH DASIA
<dead_grave> <dead_psili> <Greek_OMEGA>	: "Ὢ"	U1F6A # GREEK CAPITAL LETTER OMEGA WITH PSILI AND VARIA
<dead_grave> <Multi_key> <parenright> <Greek_OMEGA>	: "Ὢ"	U1F6A # GREEK CAPITAL LETTER OMEGA WITH PSILI AND VARIA
<Multi_key> <grave> <dead_psili> <Greek_OMEGA>	: "Ὢ"	U1F6A # GREEK CAPITAL LETTER OMEGA WITH PSILI AND VARIA
<Multi_key> <grave> <parenright> <Greek_OMEGA>	: "Ὢ"	U1F6A # GREEK CAPITAL LETTER OMEGA WITH PSILI AND VARIA
<dead_grave> <dead_dasia> <Greek_OMEGA>	: "Ὣ"	U1F6B # GREEK CAPITAL LETTER OMEGA WITH DASIA AND VARIA
<dead_grave> <Multi_key> <parenleft> <Greek_OMEGA>	: "Ὣ"	U1F6B # GREEK CAPITAL LETTER OMEGA WITH DASIA AND VARIA
<Multi_key> <grave> <dead_dasia> <Greek_OMEGA>	: "Ὣ"	U1F6B # GREEK CAPITAL LETTER OMEGA WITH DASIA AND VARIA
<Multi_key> <grave> <parenleft> <Greek_OMEGA>	: "Ὣ"	U1F6B # GREEK CAPITAL LETTER OMEGA WITH DASIA AND VARIA
<dead_acute> <dead_psili> <Greek_OMEGA>	: "Ὤ"	U1F6C # GREEK CAPITAL LETTER OMEGA WITH PSILI AND OXIA
<dead_acute> <Multi_key> <parenright> <Greek_OMEGA>	: "Ὤ"	U1F6C # GREEK CAPITAL LETTER OMEGA WITH PSILI AND OXIA
<Multi_key> <acute> <dead_psili> <Greek_OMEGA>	: "Ὤ"	U1F6C # GREEK CAPITAL LETTER OMEGA WITH PSILI AND OXIA
<Multi_key> <acute> <parenright> <Greek_OMEGA>	: "Ὤ"	U1F6C # GREEK CAPITAL LETTER OMEGA WITH PSILI AND OXIA
<Multi_key> <apostrophe> <dead_psili> <Greek_OMEGA>	: "Ὤ"	U1F6C # GREEK CAPITAL LETTER OMEGA WITH PSILI AND OXIA
<Multi_key> <apostrophe> <parenright> <Greek_OMEGA>	: "Ὤ"	U1F6C # GREEK CAPITAL LETTER OMEGA WITH PSILI AND OXIA
<dead_acute> <dead_dasia> <Greek_OMEGA>	: "Ὥ"	U1F6D # GREEK CAPITAL LETTER OMEGA WITH DASIA AND OXIA
<dead_acute> <Multi_key> <parenleft> <Greek_OMEGA>	: "Ὥ"	U1F6D # GREEK CAPITAL LETTER OMEGA WITH DASIA AND OXIA
<Multi_key> <acute> <dead_dasia> <Greek_OMEGA>	: "Ὥ"	U1F6D # GREEK CAPITAL LETTER OMEGA WITH DASIA AND OXIA
<Multi_key> <acute> <parenleft> <Greek_OMEGA>	: "Ὥ"	U1F6D # GREEK CAPITAL LETTER OMEGA WITH DASIA AND OXIA
<Multi_key> <apostrophe> <dead_dasia> <Greek_OMEGA>	: "Ὥ"	U1F6D # GREEK CAPITAL LETTER OMEGA WITH DASIA AND OXIA
<Multi_key> <apostrophe> <parenleft> <Greek_OMEGA>	: "Ὥ"	U1F6D # GREEK CAPITAL LETTER OMEGA WITH DASIA AND OXIA
<dead_tilde> <dead_psili> <Greek_OMEGA>	: "Ὦ"	U1F6E # GREEK CAPITAL LETTER OMEGA WITH PSILI AND PERISPOMENI
<dead_tilde> <Multi_key> <parenright> <Greek_OMEGA>	: "Ὦ"	U1F6E # GREEK CAPITAL LETTER OMEGA WITH PSILI AND PERISPOMENI
<Multi_key> <asciitilde> <dead_psili> <Greek_OMEGA>	: "Ὦ"	U1F6E # GREEK CAPITAL LETTER OMEGA WITH PSILI AND PERISPOMENI
<Multi_key> <asciitilde> <parenright> <Greek_OMEGA>	: "Ὦ"	U1F6E # GREEK CAPITAL LETTER OMEGA WITH PSILI AND PERISPOMENI
<dead_tilde> <dead_dasia> <Greek_OMEGA>	: "Ὧ"	U1F6F # GREEK CAPITAL LETTER OMEGA WITH DASIA AND PERISPOMENI
<dead_tilde> <Multi_key> <parenleft> <Greek_OMEGA>	: "Ὧ"	U1F6F # GREEK CAPITAL LETTER OMEGA WITH DASIA AND PERISPOMENI
<Multi_key> <asciitilde> <dead_dasia> <Greek_OMEGA>	: "Ὧ"	U1F6F # GREEK CAPITAL LETTER OMEGA WITH DASIA AND PERISPOMENI
<Multi_key> <asciitilde> <parenleft> <Greek_OMEGA>	: "Ὧ"	U1F6F # GREEK CAPITAL LETTER OMEGA WITH DASIA AND PERISPOMENI
<dead_grave> <Greek_alpha>		: "ὰ"	U1F70 # GREEK SMALL LETTER ALPHA WITH VARIA
<Multi_key> <grave> <Greek_alpha>	: "ὰ"	U1F70 # GREEK SMALL LETTER ALPHA WITH VARIA
<dead_grave> <Greek_epsilon>		: "ὲ"	U1F72 # GREEK SMALL LETTER EPSILON WITH VARIA
<Multi_key> <grave> <Greek_epsilon>	: "ὲ"	U1F72 # GREEK SMALL LETTER EPSILON WITH VARIA
<dead_grave> <Greek_eta>		: "ὴ"	U1F74 # GREEK SMALL LETTER ETA WITH VARIA
<Multi_key> <grave> <Greek_eta>		: "ὴ"	U1F74 # GREEK SMALL LETTER ETA WITH VARIA
<dead_grave> <Greek_iota>		: "ὶ"	U1F76 # GREEK SMALL LETTER IOTA WITH VARIA
<Multi_key> <grave> <Greek_iota>	: "ὶ"	U1F76 # GREEK SMALL LETTER IOTA WITH VARIA
<dead_grave> <Greek_omicron>		: "ὸ"	U1F78 # GREEK SMALL LETTER OMICRON WITH VARIA
<Multi_key> <grave> <Greek_omicron>	: "ὸ"	U1F78 # GREEK SMALL LETTER OMICRON WITH VARIA
<dead_grave> <Greek_upsilon>		: "ὺ"	U1F7A # GREEK SMALL LETTER UPSILON WITH VARIA
<Multi_key> <grave> <Greek_upsilon>	: "ὺ"	U1F7A # GREEK SMALL LETTER UPSILON WITH VARIA
<dead_grave> <Greek_omega>		: "ὼ"	U1F7C # GREEK SMALL LETTER OMEGA WITH VARIA
<Multi_key> <grave> <Greek_omega>	: "ὼ"	U1F7C # GREEK SMALL LETTER OMEGA WITH VARIA
<dead_iota> <dead_psili> <Greek_alpha>	: "ᾀ"	U1F80 # GREEK SMALL LETTER ALPHA WITH PSILI AND YPOGEGRAMMENI
<dead_iota> <Multi_key> <parenright> <Greek_alpha>	: "ᾀ"	U1F80 # GREEK SMALL LETTER ALPHA WITH PSILI AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <dead_psili> <Greek_alpha>	: "ᾀ"	U1F80 # GREEK SMALL LETTER ALPHA WITH PSILI AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <parenright> <Greek_alpha>	: "ᾀ"	U1F80 # GREEK SMALL LETTER ALPHA WITH PSILI AND YPOGEGRAMMENI
<dead_iota> <dead_dasia> <Greek_alpha>	: "ᾁ"	U1F81 # GREEK SMALL LETTER ALPHA WITH DASIA AND YPOGEGRAMMENI
<dead_iota> <Multi_key> <parenleft> <Greek_alpha>	: "ᾁ"	U1F81 # GREEK SMALL LETTER ALPHA WITH DASIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <dead_dasia> <Greek_alpha>	: "ᾁ"	U1F81 # GREEK SMALL LETTER ALPHA WITH DASIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <parenleft> <Greek_alpha>	: "ᾁ"	U1F81 # GREEK SMALL LETTER ALPHA WITH DASIA AND YPOGEGRAMMENI
<dead_iota> <dead_grave> <dead_psili> <Greek_alpha>	: "ᾂ"	U1F82 # GREEK SMALL LETTER ALPHA WITH PSILI AND VARIA AND YPOGEGRAMMENI
<dead_iota> <dead_grave> <Multi_key> <parenright> <Greek_alpha>	: "ᾂ"	U1F82 # GREEK SMALL LETTER ALPHA WITH PSILI AND VARIA AND YPOGEGRAMMENI
<dead_iota> <Multi_key> <grave> <dead_psili> <Greek_alpha>	: "ᾂ"	U1F82 # GREEK SMALL LETTER ALPHA WITH PSILI AND VARIA AND YPOGEGRAMMENI
<dead_iota> <Multi_key> <grave> <parenright> <Greek_alpha>	: "ᾂ"	U1F82 # GREEK SMALL LETTER ALPHA WITH PSILI AND VARIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <dead_grave> <dead_psili> <Greek_alpha>	: "ᾂ"	U1F82 # GREEK SMALL LETTER ALPHA WITH PSILI AND VARIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <dead_grave> <parenright> <Greek_alpha>	: "ᾂ"	U1F82 # GREEK SMALL LETTER ALPHA WITH PSILI AND VARIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <grave> <dead_psili> <Greek_alpha>	: "ᾂ"	U1F82 # GREEK SMALL LETTER ALPHA WITH PSILI AND VARIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <grave> <parenright> <Greek_alpha>	: "ᾂ"	U1F82 # GREEK SMALL LETTER ALPHA WITH PSILI AND VARIA AND YPOGEGRAMMENI
<dead_iota> <dead_grave> <dead_dasia> <Greek_alpha>	: "ᾃ"	U1F83 # GREEK SMALL LETTER ALPHA WITH DASIA AND VARIA AND YPOGEGRAMMENI
<dead_iota> <dead_grave> <Multi_key> <parenleft> <Greek_alpha>	: "ᾃ"	U1F83 # GREEK SMALL LETTER ALPHA WITH DASIA AND VARIA AND YPOGEGRAMMENI
<dead_iota> <Multi_key> <grave> <dead_dasia> <Greek_alpha>	: "ᾃ"	U1F83 # GREEK SMALL LETTER ALPHA WITH DASIA AND VARIA AND YPOGEGRAMMENI
<dead_iota> <Multi_key> <grave> <parenleft> <Greek_alpha>	: "ᾃ"	U1F83 # GREEK SMALL LETTER ALPHA WITH DASIA AND VARIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <dead_grave> <dead_dasia> <Greek_alpha>	: "ᾃ"	U1F83 # GREEK SMALL LETTER ALPHA WITH DASIA AND VARIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <dead_grave> <parenleft> <Greek_alpha>	: "ᾃ"	U1F83 # GREEK SMALL LETTER ALPHA WITH DASIA AND VARIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <grave> <dead_dasia> <Greek_alpha>	: "ᾃ"	U1F83 # GREEK SMALL LETTER ALPHA WITH DASIA AND VARIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <grave> <parenleft> <Greek_alpha>	: "ᾃ"	U1F83 # GREEK SMALL LETTER ALPHA WITH DASIA AND VARIA AND YPOGEGRAMMENI
<dead_iota> <dead_acute> <dead_psili> <Greek_alpha>	: "ᾄ"	U1F84 # GREEK SMALL LETTER ALPHA WITH PSILI AND OXIA AND YPOGEGRAMMENI
<dead_iota> <dead_acute> <Multi_key> <parenright> <Greek_alpha>	: "ᾄ"	U1F84 # GREEK SMALL LETTER ALPHA WITH PSILI AND OXIA AND YPOGEGRAMMENI
<dead_iota> <Multi_key> <apostrophe> <dead_psili> <Greek_alpha>	: "ᾄ"	U1F84 # GREEK SMALL LETTER ALPHA WITH PSILI AND OXIA AND YPOGEGRAMMENI
<dead_iota> <Multi_key> <apostrophe> <parenright> <Greek_alpha>	: "ᾄ"	U1F84 # GREEK SMALL LETTER ALPHA WITH PSILI AND OXIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <dead_acute> <dead_psili> <Greek_alpha>	: "ᾄ"	U1F84 # GREEK SMALL LETTER ALPHA WITH PSILI AND OXIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <dead_acute> <parenright> <Greek_alpha>	: "ᾄ"	U1F84 # GREEK SMALL LETTER ALPHA WITH PSILI AND OXIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <acute> <dead_psili> <Greek_alpha>	: "ᾄ"	U1F84 # GREEK SMALL LETTER ALPHA WITH PSILI AND OXIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <acute> <parenright> <Greek_alpha>	: "ᾄ"	U1F84 # GREEK SMALL LETTER ALPHA WITH PSILI AND OXIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <apostrophe> <dead_psili> <Greek_alpha>	: "ᾄ"	U1F84 # GREEK SMALL LETTER ALPHA WITH PSILI AND OXIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <apostrophe> <parenright> <Greek_alpha>	: "ᾄ"	U1F84 # GREEK SMALL LETTER ALPHA WITH PSILI AND OXIA AND YPOGEGRAMMENI
<dead_iota> <dead_acute> <dead_dasia> <Greek_alpha>	: "ᾅ"	U1F85 # GREEK SMALL LETTER ALPHA WITH DASIA AND OXIA AND YPOGEGRAMMENI
<dead_iota> <dead_acute> <Multi_key> <parenleft> <Greek_alpha>	: "ᾅ"	U1F85 # GREEK SMALL LETTER ALPHA WITH DASIA AND OXIA AND YPOGEGRAMMENI
<dead_iota> <Multi_key> <apostrophe> <dead_dasia> <Greek_alpha>	: "ᾅ"	U1F85 # GREEK SMALL LETTER ALPHA WITH DASIA AND OXIA AND YPOGEGRAMMENI
<dead_iota> <Multi_key> <apostrophe> <parenleft> <Greek_alpha>	: "ᾅ"	U1F85 # GREEK SMALL LETTER ALPHA WITH DASIA AND OXIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <dead_acute> <dead_dasia> <Greek_alpha>	: "ᾅ"	U1F85 # GREEK SMALL LETTER ALPHA WITH DASIA AND OXIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <dead_acute> <parenleft> <Greek_alpha>	: "ᾅ"	U1F85 # GREEK SMALL LETTER ALPHA WITH DASIA AND OXIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <acute> <dead_dasia> <Greek_alpha>	: "ᾅ"	U1F85 # GREEK SMALL LETTER ALPHA WITH DASIA AND OXIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <acute> <parenleft> <Greek_alpha>	: "ᾅ"	U1F85 # GREEK SMALL LETTER ALPHA WITH DASIA AND OXIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <apostrophe> <dead_dasia> <Greek_alpha>	: "ᾅ"	U1F85 # GREEK SMALL LETTER ALPHA WITH DASIA AND OXIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <apostrophe> <parenleft> <Greek_alpha>	: "ᾅ"	U1F85 # GREEK SMALL LETTER ALPHA WITH DASIA AND OXIA AND YPOGEGRAMMENI
<dead_iota> <dead_tilde> <dead_psili> <Greek_alpha>	: "ᾆ"	U1F86 # GREEK SMALL LETTER ALPHA WITH PSILI AND PERISPOMENI AND YPOGEGRAMMENI
<dead_iota> <dead_tilde> <Multi_key> <parenright> <Greek_alpha>	: "ᾆ"	U1F86 # GREEK SMALL LETTER ALPHA WITH PSILI AND PERISPOMENI AND YPOGEGRAMMENI
<dead_iota> <Multi_key> <asciitilde> <dead_psili> <Greek_alpha>	: "ᾆ"	U1F86 # GREEK SMALL LETTER ALPHA WITH PSILI AND PERISPOMENI AND YPOGEGRAMMENI
<dead_iota> <Multi_key> <asciitilde> <parenright> <Greek_alpha>	: "ᾆ"	U1F86 # GREEK SMALL LETTER ALPHA WITH PSILI AND PERISPOMENI AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <dead_tilde> <dead_psili> <Greek_alpha>	: "ᾆ"	U1F86 # GREEK SMALL LETTER ALPHA WITH PSILI AND PERISPOMENI AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <dead_tilde> <parenright> <Greek_alpha>	: "ᾆ"	U1F86 # GREEK SMALL LETTER ALPHA WITH PSILI AND PERISPOMENI AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <asciitilde> <dead_psili> <Greek_alpha>	: "ᾆ"	U1F86 # GREEK SMALL LETTER ALPHA WITH PSILI AND PERISPOMENI AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <asciitilde> <parenright> <Greek_alpha>	: "ᾆ"	U1F86 # GREEK SMALL LETTER ALPHA WITH PSILI AND PERISPOMENI AND YPOGEGRAMMENI
<dead_iota> <dead_tilde> <dead_dasia> <Greek_alpha>	: "ᾇ"	U1F87 # GREEK SMALL LETTER ALPHA WITH DASIA AND PERISPOMENI AND YPOGEGRAMMENI
<dead_iota> <dead_tilde> <Multi_key> <parenleft> <Greek_alpha>	: "ᾇ"	U1F87 # GREEK SMALL LETTER ALPHA WITH DASIA AND PERISPOMENI AND YPOGEGRAMMENI
<dead_iota> <Multi_key> <asciitilde> <dead_dasia> <Greek_alpha>	: "ᾇ"	U1F87 # GREEK SMALL LETTER ALPHA WITH DASIA AND PERISPOMENI AND YPOGEGRAMMENI
<dead_iota> <Multi_key> <asciitilde> <parenleft> <Greek_alpha>	: "ᾇ"	U1F87 # GREEK SMALL LETTER ALPHA WITH DASIA AND PERISPOMENI AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <dead_tilde> <dead_dasia> <Greek_alpha>	: "ᾇ"	U1F87 # GREEK SMALL LETTER ALPHA WITH DASIA AND PERISPOMENI AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <dead_tilde> <parenleft> <Greek_alpha>	: "ᾇ"	U1F87 # GREEK SMALL LETTER ALPHA WITH DASIA AND PERISPOMENI AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <asciitilde> <dead_dasia> <Greek_alpha>	: "ᾇ"	U1F87 # GREEK SMALL LETTER ALPHA WITH DASIA AND PERISPOMENI AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <asciitilde> <parenleft> <Greek_alpha>	: "ᾇ"	U1F87 # GREEK SMALL LETTER ALPHA WITH DASIA AND PERISPOMENI AND YPOGEGRAMMENI
<dead_iota> <dead_psili> <Greek_ALPHA>	: "ᾈ"	U1F88 # GREEK CAPITAL LETTER ALPHA WITH PSILI AND PROSGEGRAMMENI
<dead_iota> <Multi_key> <parenright> <Greek_ALPHA>	: "ᾈ"	U1F88 # GREEK CAPITAL LETTER ALPHA WITH PSILI AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <dead_psili> <Greek_ALPHA>	: "ᾈ"	U1F88 # GREEK CAPITAL LETTER ALPHA WITH PSILI AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <parenright> <Greek_ALPHA>	: "ᾈ"	U1F88 # GREEK CAPITAL LETTER ALPHA WITH PSILI AND PROSGEGRAMMENI
<dead_iota> <dead_dasia> <Greek_ALPHA>	: "ᾉ"	U1F89 # GREEK CAPITAL LETTER ALPHA WITH DASIA AND PROSGEGRAMMENI
<dead_iota> <Multi_key> <parenleft> <Greek_ALPHA>	: "ᾉ"	U1F89 # GREEK CAPITAL LETTER ALPHA WITH DASIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <dead_dasia> <Greek_ALPHA>	: "ᾉ"	U1F89 # GREEK CAPITAL LETTER ALPHA WITH DASIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <parenleft> <Greek_ALPHA>	: "ᾉ"	U1F89 # GREEK CAPITAL LETTER ALPHA WITH DASIA AND PROSGEGRAMMENI
<dead_iota> <dead_grave> <dead_psili> <Greek_ALPHA>	: "ᾊ"	U1F8A # GREEK CAPITAL LETTER ALPHA WITH PSILI AND VARIA AND PROSGEGRAMMENI
<dead_iota> <dead_grave> <Multi_key> <parenright> <Greek_ALPHA>	: "ᾊ"	U1F8A # GREEK CAPITAL LETTER ALPHA WITH PSILI AND VARIA AND PROSGEGRAMMENI
<dead_iota> <Multi_key> <grave> <dead_psili> <Greek_ALPHA>	: "ᾊ"	U1F8A # GREEK CAPITAL LETTER ALPHA WITH PSILI AND VARIA AND PROSGEGRAMMENI
<dead_iota> <Multi_key> <grave> <parenright> <Greek_ALPHA>	: "ᾊ"	U1F8A # GREEK CAPITAL LETTER ALPHA WITH PSILI AND VARIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <dead_grave> <dead_psili> <Greek_ALPHA>	: "ᾊ"	U1F8A # GREEK CAPITAL LETTER ALPHA WITH PSILI AND VARIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <dead_grave> <parenright> <Greek_ALPHA>	: "ᾊ"	U1F8A # GREEK CAPITAL LETTER ALPHA WITH PSILI AND VARIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <grave> <dead_psili> <Greek_ALPHA>	: "ᾊ"	U1F8A # GREEK CAPITAL LETTER ALPHA WITH PSILI AND VARIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <grave> <parenright> <Greek_ALPHA>	: "ᾊ"	U1F8A # GREEK CAPITAL LETTER ALPHA WITH PSILI AND VARIA AND PROSGEGRAMMENI
<dead_iota> <dead_grave> <dead_dasia> <Greek_ALPHA>	: "ᾋ"	U1F8B # GREEK CAPITAL LETTER ALPHA WITH DASIA AND VARIA AND PROSGEGRAMMENI
<dead_iota> <dead_grave> <Multi_key> <parenleft> <Greek_ALPHA>	: "ᾋ"	U1F8B # GREEK CAPITAL LETTER ALPHA WITH DASIA AND VARIA AND PROSGEGRAMMENI
<dead_iota> <Multi_key> <grave> <dead_dasia> <Greek_ALPHA>	: "ᾋ"	U1F8B # GREEK CAPITAL LETTER ALPHA WITH DASIA AND VARIA AND PROSGEGRAMMENI
<dead_iota> <Multi_key> <grave> <parenleft> <Greek_ALPHA>	: "ᾋ"	U1F8B # GREEK CAPITAL LETTER ALPHA WITH DASIA AND VARIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <dead_grave> <dead_dasia> <Greek_ALPHA>	: "ᾋ"	U1F8B # GREEK CAPITAL LETTER ALPHA WITH DASIA AND VARIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <dead_grave> <parenleft> <Greek_ALPHA>	: "ᾋ"	U1F8B # GREEK CAPITAL LETTER ALPHA WITH DASIA AND VARIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <grave> <dead_dasia> <Greek_ALPHA>	: "ᾋ"	U1F8B # GREEK CAPITAL LETTER ALPHA WITH DASIA AND VARIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <grave> <parenleft> <Greek_ALPHA>	: "ᾋ"	U1F8B # GREEK CAPITAL LETTER ALPHA WITH DASIA AND VARIA AND PROSGEGRAMMENI
<dead_iota> <dead_acute> <dead_psili> <Greek_ALPHA>	: "ᾌ"	U1F8C # GREEK CAPITAL LETTER ALPHA WITH PSILI AND OXIA AND PROSGEGRAMMENI
<dead_iota> <dead_acute> <Multi_key> <parenright> <Greek_ALPHA>	: "ᾌ"	U1F8C # GREEK CAPITAL LETTER ALPHA WITH PSILI AND OXIA AND PROSGEGRAMMENI
<dead_iota> <Multi_key> <apostrophe> <dead_psili> <Greek_ALPHA>	: "ᾌ"	U1F8C # GREEK CAPITAL LETTER ALPHA WITH PSILI AND OXIA AND PROSGEGRAMMENI
<dead_iota> <Multi_key> <apostrophe> <parenright> <Greek_ALPHA>	: "ᾌ"	U1F8C # GREEK CAPITAL LETTER ALPHA WITH PSILI AND OXIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <dead_acute> <dead_psili> <Greek_ALPHA>	: "ᾌ"	U1F8C # GREEK CAPITAL LETTER ALPHA WITH PSILI AND OXIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <dead_acute> <parenright> <Greek_ALPHA>	: "ᾌ"	U1F8C # GREEK CAPITAL LETTER ALPHA WITH PSILI AND OXIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <acute> <dead_psili> <Greek_ALPHA>	: "ᾌ"	U1F8C # GREEK CAPITAL LETTER ALPHA WITH PSILI AND OXIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <acute> <parenright> <Greek_ALPHA>	: "ᾌ"	U1F8C # GREEK CAPITAL LETTER ALPHA WITH PSILI AND OXIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <apostrophe> <dead_psili> <Greek_ALPHA>	: "ᾌ"	U1F8C # GREEK CAPITAL LETTER ALPHA WITH PSILI AND OXIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <apostrophe> <parenright> <Greek_ALPHA>	: "ᾌ"	U1F8C # GREEK CAPITAL LETTER ALPHA WITH PSILI AND OXIA AND PROSGEGRAMMENI
<dead_iota> <dead_acute> <dead_dasia> <Greek_ALPHA>	: "ᾍ"	U1F8D # GREEK CAPITAL LETTER ALPHA WITH DASIA AND OXIA AND PROSGEGRAMMENI
<dead_iota> <dead_acute> <Multi_key> <parenleft> <Greek_ALPHA>	: "ᾍ"	U1F8D # GREEK CAPITAL LETTER ALPHA WITH DASIA AND OXIA AND PROSGEGRAMMENI
<dead_iota> <Multi_key> <apostrophe> <dead_dasia> <Greek_ALPHA>	: "ᾍ"	U1F8D # GREEK CAPITAL LETTER ALPHA WITH DASIA AND OXIA AND PROSGEGRAMMENI
<dead_iota> <Multi_key> <apostrophe> <parenleft> <Greek_ALPHA>	: "ᾍ"	U1F8D # GREEK CAPITAL LETTER ALPHA WITH DASIA AND OXIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <dead_acute> <dead_dasia> <Greek_ALPHA>	: "ᾍ"	U1F8D # GREEK CAPITAL LETTER ALPHA WITH DASIA AND OXIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <dead_acute> <parenleft> <Greek_ALPHA>	: "ᾍ"	U1F8D # GREEK CAPITAL LETTER ALPHA WITH DASIA AND OXIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <acute> <dead_dasia> <Greek_ALPHA>	: "ᾍ"	U1F8D # GREEK CAPITAL LETTER ALPHA WITH DASIA AND OXIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <acute> <parenleft> <Greek_ALPHA>	: "ᾍ"	U1F8D # GREEK CAPITAL LETTER ALPHA WITH DASIA AND OXIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <apostrophe> <dead_dasia> <Greek_ALPHA>	: "ᾍ"	U1F8D # GREEK CAPITAL LETTER ALPHA WITH DASIA AND OXIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <apostrophe> <parenleft> <Greek_ALPHA>	: "ᾍ"	U1F8D # GREEK CAPITAL LETTER ALPHA WITH DASIA AND OXIA AND PROSGEGRAMMENI
<dead_iota> <dead_tilde> <dead_psili> <Greek_ALPHA>	: "ᾎ"	U1F8E # GREEK CAPITAL LETTER ALPHA WITH PSILI AND PERISPOMENI AND PROSGEGRAMMENI
<dead_iota> <dead_tilde> <Multi_key> <parenright> <Greek_ALPHA>	: "ᾎ"	U1F8E # GREEK CAPITAL LETTER ALPHA WITH PSILI AND PERISPOMENI AND PROSGEGRAMMENI
<dead_iota> <Multi_key> <asciitilde> <dead_psili> <Greek_ALPHA>	: "ᾎ"	U1F8E # GREEK CAPITAL LETTER ALPHA WITH PSILI AND PERISPOMENI AND PROSGEGRAMMENI
<dead_iota> <Multi_key> <asciitilde> <parenright> <Greek_ALPHA>	: "ᾎ"	U1F8E # GREEK CAPITAL LETTER ALPHA WITH PSILI AND PERISPOMENI AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <dead_tilde> <dead_psili> <Greek_ALPHA>	: "ᾎ"	U1F8E # GREEK CAPITAL LETTER ALPHA WITH PSILI AND PERISPOMENI AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <dead_tilde> <parenright> <Greek_ALPHA>	: "ᾎ"	U1F8E # GREEK CAPITAL LETTER ALPHA WITH PSILI AND PERISPOMENI AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <asciitilde> <dead_psili> <Greek_ALPHA>	: "ᾎ"	U1F8E # GREEK CAPITAL LETTER ALPHA WITH PSILI AND PERISPOMENI AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <asciitilde> <parenright> <Greek_ALPHA>	: "ᾎ"	U1F8E # GREEK CAPITAL LETTER ALPHA WITH PSILI AND PERISPOMENI AND PROSGEGRAMMENI
<dead_iota> <dead_tilde> <dead_dasia> <Greek_ALPHA>	: "ᾏ"	U1F8F # GREEK CAPITAL LETTER ALPHA WITH DASIA AND PERISPOMENI AND PROSGEGRAMMENI
<dead_iota> <dead_tilde> <Multi_key> <parenleft> <Greek_ALPHA>	: "ᾏ"	U1F8F # GREEK CAPITAL LETTER ALPHA WITH DASIA AND PERISPOMENI AND PROSGEGRAMMENI
<dead_iota> <Multi_key> <asciitilde> <dead_dasia> <Greek_ALPHA>	: "ᾏ"	U1F8F # GREEK CAPITAL LETTER ALPHA WITH DASIA AND PERISPOMENI AND PROSGEGRAMMENI
<dead_iota> <Multi_key> <asciitilde> <parenleft> <Greek_ALPHA>	: "ᾏ"	U1F8F # GREEK CAPITAL LETTER ALPHA WITH DASIA AND PERISPOMENI AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <dead_tilde> <dead_dasia> <Greek_ALPHA>	: "ᾏ"	U1F8F # GREEK CAPITAL LETTER ALPHA WITH DASIA AND PERISPOMENI AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <dead_tilde> <parenleft> <Greek_ALPHA>	: "ᾏ"	U1F8F # GREEK CAPITAL LETTER ALPHA WITH DASIA AND PERISPOMENI AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <asciitilde> <dead_dasia> <Greek_ALPHA>	: "ᾏ"	U1F8F # GREEK CAPITAL LETTER ALPHA WITH DASIA AND PERISPOMENI AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <asciitilde> <parenleft> <Greek_ALPHA>	: "ᾏ"	U1F8F # GREEK CAPITAL LETTER ALPHA WITH DASIA AND PERISPOMENI AND PROSGEGRAMMENI
<dead_iota> <dead_psili> <Greek_eta>	: "ᾐ"	U1F90 # GREEK SMALL LETTER ETA WITH PSILI AND YPOGEGRAMMENI
<dead_iota> <Multi_key> <parenright> <Greek_eta>	: "ᾐ"	U1F90 # GREEK SMALL LETTER ETA WITH PSILI AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <dead_psili> <Greek_eta>	: "ᾐ"	U1F90 # GREEK SMALL LETTER ETA WITH PSILI AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <parenright> <Greek_eta>	: "ᾐ"	U1F90 # GREEK SMALL LETTER ETA WITH PSILI AND YPOGEGRAMMENI
<dead_iota> <dead_dasia> <Greek_eta>	: "ᾑ"	U1F91 # GREEK SMALL LETTER ETA WITH DASIA AND YPOGEGRAMMENI
<dead_iota> <Multi_key> <parenleft> <Greek_eta>	: "ᾑ"	U1F91 # GREEK SMALL LETTER ETA WITH DASIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <dead_dasia> <Greek_eta>	: "ᾑ"	U1F91 # GREEK SMALL LETTER ETA WITH DASIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <parenleft> <Greek_eta>	: "ᾑ"	U1F91 # GREEK SMALL LETTER ETA WITH DASIA AND YPOGEGRAMMENI
<dead_iota> <dead_grave> <dead_psili> <Greek_eta>	: "ᾒ"	U1F92 # GREEK SMALL LETTER ETA WITH PSILI AND VARIA AND YPOGEGRAMMENI
<dead_iota> <dead_grave> <Multi_key> <parenright> <Greek_eta>	: "ᾒ"	U1F92 # GREEK SMALL LETTER ETA WITH PSILI AND VARIA AND YPOGEGRAMMENI
<dead_iota> <Multi_key> <grave> <dead_psili> <Greek_eta>	: "ᾒ"	U1F92 # GREEK SMALL LETTER ETA WITH PSILI AND VARIA AND YPOGEGRAMMENI
<dead_iota> <Multi_key> <grave> <parenright> <Greek_eta>	: "ᾒ"	U1F92 # GREEK SMALL LETTER ETA WITH PSILI AND VARIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <dead_grave> <dead_psili> <Greek_eta>	: "ᾒ"	U1F92 # GREEK SMALL LETTER ETA WITH PSILI AND VARIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <dead_grave> <parenright> <Greek_eta>	: "ᾒ"	U1F92 # GREEK SMALL LETTER ETA WITH PSILI AND VARIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <grave> <dead_psili> <Greek_eta>	: "ᾒ"	U1F92 # GREEK SMALL LETTER ETA WITH PSILI AND VARIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <grave> <parenright> <Greek_eta>	: "ᾒ"	U1F92 # GREEK SMALL LETTER ETA WITH PSILI AND VARIA AND YPOGEGRAMMENI
<dead_iota> <dead_grave> <dead_dasia> <Greek_eta>	: "ᾓ"	U1F93 # GREEK SMALL LETTER ETA WITH DASIA AND VARIA AND YPOGEGRAMMENI
<dead_iota> <dead_grave> <Multi_key> <parenleft> <Greek_eta>	: "ᾓ"	U1F93 # GREEK SMALL LETTER ETA WITH DASIA AND VARIA AND YPOGEGRAMMENI
<dead_iota> <Multi_key> <grave> <dead_dasia> <Greek_eta>	: "ᾓ"	U1F93 # GREEK SMALL LETTER ETA WITH DASIA AND VARIA AND YPOGEGRAMMENI
<dead_iota> <Multi_key> <grave> <parenleft> <Greek_eta>	: "ᾓ"	U1F93 # GREEK SMALL LETTER ETA WITH DASIA AND VARIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <dead_grave> <dead_dasia> <Greek_eta>	: "ᾓ"	U1F93 # GREEK SMALL LETTER ETA WITH DASIA AND VARIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <dead_grave> <parenleft> <Greek_eta>	: "ᾓ"	U1F93 # GREEK SMALL LETTER ETA WITH DASIA AND VARIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <grave> <dead_dasia> <Greek_eta>	: "ᾓ"	U1F93 # GREEK SMALL LETTER ETA WITH DASIA AND VARIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <grave> <parenleft> <Greek_eta>	: "ᾓ"	U1F93 # GREEK SMALL LETTER ETA WITH DASIA AND VARIA AND YPOGEGRAMMENI
<dead_iota> <dead_acute> <dead_psili> <Greek_eta>	: "ᾔ"	U1F94 # GREEK SMALL LETTER ETA WITH PSILI AND OXIA AND YPOGEGRAMMENI
<dead_iota> <dead_acute> <Multi_key> <parenright> <Greek_eta>	: "ᾔ"	U1F94 # GREEK SMALL LETTER ETA WITH PSILI AND OXIA AND YPOGEGRAMMENI
<dead_iota> <Multi_key> <apostrophe> <dead_psili> <Greek_eta>	: "ᾔ"	U1F94 # GREEK SMALL LETTER ETA WITH PSILI AND OXIA AND YPOGEGRAMMENI
<dead_iota> <Multi_key> <apostrophe> <parenright> <Greek_eta>	: "ᾔ"	U1F94 # GREEK SMALL LETTER ETA WITH PSILI AND OXIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <dead_acute> <dead_psili> <Greek_eta>	: "ᾔ"	U1F94 # GREEK SMALL LETTER ETA WITH PSILI AND OXIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <dead_acute> <parenright> <Greek_eta>	: "ᾔ"	U1F94 # GREEK SMALL LETTER ETA WITH PSILI AND OXIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <acute> <dead_psili> <Greek_eta>	: "ᾔ"	U1F94 # GREEK SMALL LETTER ETA WITH PSILI AND OXIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <acute> <parenright> <Greek_eta>	: "ᾔ"	U1F94 # GREEK SMALL LETTER ETA WITH PSILI AND OXIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <apostrophe> <dead_psili> <Greek_eta>	: "ᾔ"	U1F94 # GREEK SMALL LETTER ETA WITH PSILI AND OXIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <apostrophe> <parenright> <Greek_eta>	: "ᾔ"	U1F94 # GREEK SMALL LETTER ETA WITH PSILI AND OXIA AND YPOGEGRAMMENI
<dead_iota> <dead_acute> <dead_dasia> <Greek_eta>	: "ᾕ"	U1F95 # GREEK SMALL LETTER ETA WITH DASIA AND OXIA AND YPOGEGRAMMENI
<dead_iota> <dead_acute> <Multi_key> <parenleft> <Greek_eta>	: "ᾕ"	U1F95 # GREEK SMALL LETTER ETA WITH DASIA AND OXIA AND YPOGEGRAMMENI
<dead_iota> <Multi_key> <apostrophe> <dead_dasia> <Greek_eta>	: "ᾕ"	U1F95 # GREEK SMALL LETTER ETA WITH DASIA AND OXIA AND YPOGEGRAMMENI
<dead_iota> <Multi_key> <apostrophe> <parenleft> <Greek_eta>	: "ᾕ"	U1F95 # GREEK SMALL LETTER ETA WITH DASIA AND OXIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <dead_acute> <dead_dasia> <Greek_eta>	: "ᾕ"	U1F95 # GREEK SMALL LETTER ETA WITH DASIA AND OXIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <dead_acute> <parenleft> <Greek_eta>	: "ᾕ"	U1F95 # GREEK SMALL LETTER ETA WITH DASIA AND OXIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <acute> <dead_dasia> <Greek_eta>	: "ᾕ"	U1F95 # GREEK SMALL LETTER ETA WITH DASIA AND OXIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <acute> <parenleft> <Greek_eta>	: "ᾕ"	U1F95 # GREEK SMALL LETTER ETA WITH DASIA AND OXIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <apostrophe> <dead_dasia> <Greek_eta>	: "ᾕ"	U1F95 # GREEK SMALL LETTER ETA WITH DASIA AND OXIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <apostrophe> <parenleft> <Greek_eta>	: "ᾕ"	U1F95 # GREEK SMALL LETTER ETA WITH DASIA AND OXIA AND YPOGEGRAMMENI
<dead_iota> <dead_tilde> <dead_psili> <Greek_eta>	: "ᾖ"	U1F96 # GREEK SMALL LETTER ETA WITH PSILI AND PERISPOMENI AND YPOGEGRAMMENI
<dead_iota> <dead_tilde> <Multi_key> <parenright> <Greek_eta>	: "ᾖ"	U1F96 # GREEK SMALL LETTER ETA WITH PSILI AND PERISPOMENI AND YPOGEGRAMMENI
<dead_iota> <Multi_key> <asciitilde> <dead_psili> <Greek_eta>	: "ᾖ"	U1F96 # GREEK SMALL LETTER ETA WITH PSILI AND PERISPOMENI AND YPOGEGRAMMENI
<dead_iota> <Multi_key> <asciitilde> <parenright> <Greek_eta>	: "ᾖ"	U1F96 # GREEK SMALL LETTER ETA WITH PSILI AND PERISPOMENI AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <dead_tilde> <dead_psili> <Greek_eta>	: "ᾖ"	U1F96 # GREEK SMALL LETTER ETA WITH PSILI AND PERISPOMENI AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <dead_tilde> <parenright> <Greek_eta>	: "ᾖ"	U1F96 # GREEK SMALL LETTER ETA WITH PSILI AND PERISPOMENI AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <asciitilde> <dead_psili> <Greek_eta>	: "ᾖ"	U1F96 # GREEK SMALL LETTER ETA WITH PSILI AND PERISPOMENI AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <asciitilde> <parenright> <Greek_eta>	: "ᾖ"	U1F96 # GREEK SMALL LETTER ETA WITH PSILI AND PERISPOMENI AND YPOGEGRAMMENI
<dead_iota> <dead_tilde> <dead_dasia> <Greek_eta>	: "ᾗ"	U1F97 # GREEK SMALL LETTER ETA WITH DASIA AND PERISPOMENI AND YPOGEGRAMMENI
<dead_iota> <dead_tilde> <Multi_key> <parenleft> <Greek_eta>	: "ᾗ"	U1F97 # GREEK SMALL LETTER ETA WITH DASIA AND PERISPOMENI AND YPOGEGRAMMENI
<dead_iota> <Multi_key> <asciitilde> <dead_dasia> <Greek_eta>	: "ᾗ"	U1F97 # GREEK SMALL LETTER ETA WITH DASIA AND PERISPOMENI AND YPOGEGRAMMENI
<dead_iota> <Multi_key> <asciitilde> <parenleft> <Greek_eta>	: "ᾗ"	U1F97 # GREEK SMALL LETTER ETA WITH DASIA AND PERISPOMENI AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <dead_tilde> <dead_dasia> <Greek_eta>	: "ᾗ"	U1F97 # GREEK SMALL LETTER ETA WITH DASIA AND PERISPOMENI AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <dead_tilde> <parenleft> <Greek_eta>	: "ᾗ"	U1F97 # GREEK SMALL LETTER ETA WITH DASIA AND PERISPOMENI AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <asciitilde> <dead_dasia> <Greek_eta>	: "ᾗ"	U1F97 # GREEK SMALL LETTER ETA WITH DASIA AND PERISPOMENI AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <asciitilde> <parenleft> <Greek_eta>	: "ᾗ"	U1F97 # GREEK SMALL LETTER ETA WITH DASIA AND PERISPOMENI AND YPOGEGRAMMENI
<dead_iota> <dead_psili> <Greek_ETA>	: "ᾘ"	U1F98 # GREEK CAPITAL LETTER ETA WITH PSILI AND PROSGEGRAMMENI
<dead_iota> <Multi_key> <parenright> <Greek_ETA>	: "ᾘ"	U1F98 # GREEK CAPITAL LETTER ETA WITH PSILI AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <dead_psili> <Greek_ETA>	: "ᾘ"	U1F98 # GREEK CAPITAL LETTER ETA WITH PSILI AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <parenright> <Greek_ETA>	: "ᾘ"	U1F98 # GREEK CAPITAL LETTER ETA WITH PSILI AND PROSGEGRAMMENI
<dead_iota> <dead_dasia> <Greek_ETA>	: "ᾙ"	U1F99 # GREEK CAPITAL LETTER ETA WITH DASIA AND PROSGEGRAMMENI
<dead_iota> <Multi_key> <parenleft> <Greek_ETA>	: "ᾙ"	U1F99 # GREEK CAPITAL LETTER ETA WITH DASIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <dead_dasia> <Greek_ETA>	: "ᾙ"	U1F99 # GREEK CAPITAL LETTER ETA WITH DASIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <parenleft> <Greek_ETA>	: "ᾙ"	U1F99 # GREEK CAPITAL LETTER ETA WITH DASIA AND PROSGEGRAMMENI
<dead_iota> <dead_grave> <dead_psili> <Greek_ETA>	: "ᾚ"	U1F9A # GREEK CAPITAL LETTER ETA WITH PSILI AND VARIA AND PROSGEGRAMMENI
<dead_iota> <dead_grave> <Multi_key> <parenright> <Greek_ETA>	: "ᾚ"	U1F9A # GREEK CAPITAL LETTER ETA WITH PSILI AND VARIA AND PROSGEGRAMMENI
<dead_iota> <Multi_key> <grave> <dead_psili> <Greek_ETA>	: "ᾚ"	U1F9A # GREEK CAPITAL LETTER ETA WITH PSILI AND VARIA AND PROSGEGRAMMENI
<dead_iota> <Multi_key> <grave> <parenright> <Greek_ETA>	: "ᾚ"	U1F9A # GREEK CAPITAL LETTER ETA WITH PSILI AND VARIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <dead_grave> <dead_psili> <Greek_ETA>	: "ᾚ"	U1F9A # GREEK CAPITAL LETTER ETA WITH PSILI AND VARIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <dead_grave> <parenright> <Greek_ETA>	: "ᾚ"	U1F9A # GREEK CAPITAL LETTER ETA WITH PSILI AND VARIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <grave> <dead_psili> <Greek_ETA>	: "ᾚ"	U1F9A # GREEK CAPITAL LETTER ETA WITH PSILI AND VARIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <grave> <parenright> <Greek_ETA>	: "ᾚ"	U1F9A # GREEK CAPITAL LETTER ETA WITH PSILI AND VARIA AND PROSGEGRAMMENI
<dead_iota> <dead_grave> <dead_dasia> <Greek_ETA>	: "ᾛ"	U1F9B # GREEK CAPITAL LETTER ETA WITH DASIA AND VARIA AND PROSGEGRAMMENI
<dead_iota> <dead_grave> <Multi_key> <parenleft> <Greek_ETA>	: "ᾛ"	U1F9B # GREEK CAPITAL LETTER ETA WITH DASIA AND VARIA AND PROSGEGRAMMENI
<dead_iota> <Multi_key> <grave> <dead_dasia> <Greek_ETA>	: "ᾛ"	U1F9B # GREEK CAPITAL LETTER ETA WITH DASIA AND VARIA AND PROSGEGRAMMENI
<dead_iota> <Multi_key> <grave> <parenleft> <Greek_ETA>	: "ᾛ"	U1F9B # GREEK CAPITAL LETTER ETA WITH DASIA AND VARIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <dead_grave> <dead_dasia> <Greek_ETA>	: "ᾛ"	U1F9B # GREEK CAPITAL LETTER ETA WITH DASIA AND VARIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <dead_grave> <parenleft> <Greek_ETA>	: "ᾛ"	U1F9B # GREEK CAPITAL LETTER ETA WITH DASIA AND VARIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <grave> <dead_dasia> <Greek_ETA>	: "ᾛ"	U1F9B # GREEK CAPITAL LETTER ETA WITH DASIA AND VARIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <grave> <parenleft> <Greek_ETA>	: "ᾛ"	U1F9B # GREEK CAPITAL LETTER ETA WITH DASIA AND VARIA AND PROSGEGRAMMENI
<dead_iota> <dead_acute> <dead_psili> <Greek_ETA>	: "ᾜ"	U1F9C # GREEK CAPITAL LETTER ETA WITH PSILI AND OXIA AND PROSGEGRAMMENI
<dead_iota> <dead_acute> <Multi_key> <parenright> <Greek_ETA>	: "ᾜ"	U1F9C # GREEK CAPITAL LETTER ETA WITH PSILI AND OXIA AND PROSGEGRAMMENI
<dead_iota> <Multi_key> <apostrophe> <dead_psili> <Greek_ETA>	: "ᾜ"	U1F9C # GREEK CAPITAL LETTER ETA WITH PSILI AND OXIA AND PROSGEGRAMMENI
<dead_iota> <Multi_key> <apostrophe> <parenright> <Greek_ETA>	: "ᾜ"	U1F9C # GREEK CAPITAL LETTER ETA WITH PSILI AND OXIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <dead_acute> <dead_psili> <Greek_ETA>	: "ᾜ"	U1F9C # GREEK CAPITAL LETTER ETA WITH PSILI AND OXIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <dead_acute> <parenright> <Greek_ETA>	: "ᾜ"	U1F9C # GREEK CAPITAL LETTER ETA WITH PSILI AND OXIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <acute> <dead_psili> <Greek_ETA>	: "ᾜ"	U1F9C # GREEK CAPITAL LETTER ETA WITH PSILI AND OXIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <acute> <parenright> <Greek_ETA>	: "ᾜ"	U1F9C # GREEK CAPITAL LETTER ETA WITH PSILI AND OXIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <apostrophe> <dead_psili> <Greek_ETA>	: "ᾜ"	U1F9C # GREEK CAPITAL LETTER ETA WITH PSILI AND OXIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <apostrophe> <parenright> <Greek_ETA>	: "ᾜ"	U1F9C # GREEK CAPITAL LETTER ETA WITH PSILI AND OXIA AND PROSGEGRAMMENI
<dead_iota> <dead_acute> <dead_dasia> <Greek_ETA>	: "ᾝ"	U1F9D # GREEK CAPITAL LETTER ETA WITH DASIA AND OXIA AND PROSGEGRAMMENI
<dead_iota> <dead_acute> <Multi_key> <parenleft> <Greek_ETA>	: "ᾝ"	U1F9D # GREEK CAPITAL LETTER ETA WITH DASIA AND OXIA AND PROSGEGRAMMENI
<dead_iota> <Multi_key> <apostrophe> <dead_dasia> <Greek_ETA>	: "ᾝ"	U1F9D # GREEK CAPITAL LETTER ETA WITH DASIA AND OXIA AND PROSGEGRAMMENI
<dead_iota> <Multi_key> <apostrophe> <parenleft> <Greek_ETA>	: "ᾝ"	U1F9D # GREEK CAPITAL LETTER ETA WITH DASIA AND OXIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <dead_acute> <dead_dasia> <Greek_ETA>	: "ᾝ"	U1F9D # GREEK CAPITAL LETTER ETA WITH DASIA AND OXIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <dead_acute> <parenleft> <Greek_ETA>	: "ᾝ"	U1F9D # GREEK CAPITAL LETTER ETA WITH DASIA AND OXIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <acute> <dead_dasia> <Greek_ETA>	: "ᾝ"	U1F9D # GREEK CAPITAL LETTER ETA WITH DASIA AND OXIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <acute> <parenleft> <Greek_ETA>	: "ᾝ"	U1F9D # GREEK CAPITAL LETTER ETA WITH DASIA AND OXIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <apostrophe> <dead_dasia> <Greek_ETA>	: "ᾝ"	U1F9D # GREEK CAPITAL LETTER ETA WITH DASIA AND OXIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <apostrophe> <parenleft> <Greek_ETA>	: "ᾝ"	U1F9D # GREEK CAPITAL LETTER ETA WITH DASIA AND OXIA AND PROSGEGRAMMENI
<dead_iota> <dead_tilde> <dead_psili> <Greek_ETA>	: "ᾞ"	U1F9E # GREEK CAPITAL LETTER ETA WITH PSILI AND PERISPOMENI AND PROSGEGRAMMENI
<dead_iota> <dead_tilde> <Multi_key> <parenright> <Greek_ETA>	: "ᾞ"	U1F9E # GREEK CAPITAL LETTER ETA WITH PSILI AND PERISPOMENI AND PROSGEGRAMMENI
<dead_iota> <Multi_key> <asciitilde> <dead_psili> <Greek_ETA>	: "ᾞ"	U1F9E # GREEK CAPITAL LETTER ETA WITH PSILI AND PERISPOMENI AND PROSGEGRAMMENI
<dead_iota> <Multi_key> <asciitilde> <parenright> <Greek_ETA>	: "ᾞ"	U1F9E # GREEK CAPITAL LETTER ETA WITH PSILI AND PERISPOMENI AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <dead_tilde> <dead_psili> <Greek_ETA>	: "ᾞ"	U1F9E # GREEK CAPITAL LETTER ETA WITH PSILI AND PERISPOMENI AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <dead_tilde> <parenright> <Greek_ETA>	: "ᾞ"	U1F9E # GREEK CAPITAL LETTER ETA WITH PSILI AND PERISPOMENI AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <asciitilde> <dead_psili> <Greek_ETA>	: "ᾞ"	U1F9E # GREEK CAPITAL LETTER ETA WITH PSILI AND PERISPOMENI AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <asciitilde> <parenright> <Greek_ETA>	: "ᾞ"	U1F9E # GREEK CAPITAL LETTER ETA WITH PSILI AND PERISPOMENI AND PROSGEGRAMMENI
<dead_iota> <dead_tilde> <dead_dasia> <Greek_ETA>	: "ᾟ"	U1F9F # GREEK CAPITAL LETTER ETA WITH DASIA AND PERISPOMENI AND PROSGEGRAMMENI
<dead_iota> <dead_tilde> <Multi_key> <parenleft> <Greek_ETA>	: "ᾟ"	U1F9F # GREEK CAPITAL LETTER ETA WITH DASIA AND PERISPOMENI AND PROSGEGRAMMENI
<dead_iota> <Multi_key> <asciitilde> <dead_dasia> <Greek_ETA>	: "ᾟ"	U1F9F # GREEK CAPITAL LETTER ETA WITH DASIA AND PERISPOMENI AND PROSGEGRAMMENI
<dead_iota> <Multi_key> <asciitilde> <parenleft> <Greek_ETA>	: "ᾟ"	U1F9F # GREEK CAPITAL LETTER ETA WITH DASIA AND PERISPOMENI AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <dead_tilde> <dead_dasia> <Greek_ETA>	: "ᾟ"	U1F9F # GREEK CAPITAL LETTER ETA WITH DASIA AND PERISPOMENI AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <dead_tilde> <parenleft> <Greek_ETA>	: "ᾟ"	U1F9F # GREEK CAPITAL LETTER ETA WITH DASIA AND PERISPOMENI AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <asciitilde> <dead_dasia> <Greek_ETA>	: "ᾟ"	U1F9F # GREEK CAPITAL LETTER ETA WITH DASIA AND PERISPOMENI AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <asciitilde> <parenleft> <Greek_ETA>	: "ᾟ"	U1F9F # GREEK CAPITAL LETTER ETA WITH DASIA AND PERISPOMENI AND PROSGEGRAMMENI
<dead_iota> <dead_psili> <Greek_omega>	: "ᾠ"	U1FA0 # GREEK SMALL LETTER OMEGA WITH PSILI AND YPOGEGRAMMENI
<dead_iota> <Multi_key> <parenright> <Greek_omega>	: "ᾠ"	U1FA0 # GREEK SMALL LETTER OMEGA WITH PSILI AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <dead_psili> <Greek_omega>	: "ᾠ"	U1FA0 # GREEK SMALL LETTER OMEGA WITH PSILI AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <parenright> <Greek_omega>	: "ᾠ"	U1FA0 # GREEK SMALL LETTER OMEGA WITH PSILI AND YPOGEGRAMMENI
<dead_iota> <dead_dasia> <Greek_omega>	: "ᾡ"	U1FA1 # GREEK SMALL LETTER OMEGA WITH DASIA AND YPOGEGRAMMENI
<dead_iota> <Multi_key> <parenleft> <Greek_omega>	: "ᾡ"	U1FA1 # GREEK SMALL LETTER OMEGA WITH DASIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <dead_dasia> <Greek_omega>	: "ᾡ"	U1FA1 # GREEK SMALL LETTER OMEGA WITH DASIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <parenleft> <Greek_omega>	: "ᾡ"	U1FA1 # GREEK SMALL LETTER OMEGA WITH DASIA AND YPOGEGRAMMENI
<dead_iota> <dead_grave> <dead_psili> <Greek_omega>	: "ᾢ"	U1FA2 # GREEK SMALL LETTER OMEGA WITH PSILI AND VARIA AND YPOGEGRAMMENI
<dead_iota> <dead_grave> <Multi_key> <parenright> <Greek_omega>	: "ᾢ"	U1FA2 # GREEK SMALL LETTER OMEGA WITH PSILI AND VARIA AND YPOGEGRAMMENI
<dead_iota> <Multi_key> <grave> <dead_psili> <Greek_omega>	: "ᾢ"	U1FA2 # GREEK SMALL LETTER OMEGA WITH PSILI AND VARIA AND YPOGEGRAMMENI
<dead_iota> <Multi_key> <grave> <parenright> <Greek_omega>	: "ᾢ"	U1FA2 # GREEK SMALL LETTER OMEGA WITH PSILI AND VARIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <dead_grave> <dead_psili> <Greek_omega>	: "ᾢ"	U1FA2 # GREEK SMALL LETTER OMEGA WITH PSILI AND VARIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <dead_grave> <parenright> <Greek_omega>	: "ᾢ"	U1FA2 # GREEK SMALL LETTER OMEGA WITH PSILI AND VARIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <grave> <dead_psili> <Greek_omega>	: "ᾢ"	U1FA2 # GREEK SMALL LETTER OMEGA WITH PSILI AND VARIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <grave> <parenright> <Greek_omega>	: "ᾢ"	U1FA2 # GREEK SMALL LETTER OMEGA WITH PSILI AND VARIA AND YPOGEGRAMMENI
<dead_iota> <dead_grave> <dead_dasia> <Greek_omega>	: "ᾣ"	U1FA3 # GREEK SMALL LETTER OMEGA WITH DASIA AND VARIA AND YPOGEGRAMMENI
<dead_iota> <dead_grave> <Multi_key> <parenleft> <Greek_omega>	: "ᾣ"	U1FA3 # GREEK SMALL LETTER OMEGA WITH DASIA AND VARIA AND YPOGEGRAMMENI
<dead_iota> <Multi_key> <grave> <dead_dasia> <Greek_omega>	: "ᾣ"	U1FA3 # GREEK SMALL LETTER OMEGA WITH DASIA AND VARIA AND YPOGEGRAMMENI
<dead_iota> <Multi_key> <grave> <parenleft> <Greek_omega>	: "ᾣ"	U1FA3 # GREEK SMALL LETTER OMEGA WITH DASIA AND VARIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <dead_grave> <dead_dasia> <Greek_omega>	: "ᾣ"	U1FA3 # GREEK SMALL LETTER OMEGA WITH DASIA AND VARIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <dead_grave> <parenleft> <Greek_omega>	: "ᾣ"	U1FA3 # GREEK SMALL LETTER OMEGA WITH DASIA AND VARIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <grave> <dead_dasia> <Greek_omega>	: "ᾣ"	U1FA3 # GREEK SMALL LETTER OMEGA WITH DASIA AND VARIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <grave> <parenleft> <Greek_omega>	: "ᾣ"	U1FA3 # GREEK SMALL LETTER OMEGA WITH DASIA AND VARIA AND YPOGEGRAMMENI
<dead_iota> <dead_acute> <dead_psili> <Greek_omega>	: "ᾤ"	U1FA4 # GREEK SMALL LETTER OMEGA WITH PSILI AND OXIA AND YPOGEGRAMMENI
<dead_iota> <dead_acute> <Multi_key> <parenright> <Greek_omega>	: "ᾤ"	U1FA4 # GREEK SMALL LETTER OMEGA WITH PSILI AND OXIA AND YPOGEGRAMMENI
<dead_iota> <Multi_key> <apostrophe> <dead_psili> <Greek_omega>	: "ᾤ"	U1FA4 # GREEK SMALL LETTER OMEGA WITH PSILI AND OXIA AND YPOGEGRAMMENI
<dead_iota> <Multi_key> <apostrophe> <parenright> <Greek_omega>	: "ᾤ"	U1FA4 # GREEK SMALL LETTER OMEGA WITH PSILI AND OXIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <dead_acute> <dead_psili> <Greek_omega>	: "ᾤ"	U1FA4 # GREEK SMALL LETTER OMEGA WITH PSILI AND OXIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <dead_acute> <parenright> <Greek_omega>	: "ᾤ"	U1FA4 # GREEK SMALL LETTER OMEGA WITH PSILI AND OXIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <acute> <dead_psili> <Greek_omega>	: "ᾤ"	U1FA4 # GREEK SMALL LETTER OMEGA WITH PSILI AND OXIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <acute> <parenright> <Greek_omega>	: "ᾤ"	U1FA4 # GREEK SMALL LETTER OMEGA WITH PSILI AND OXIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <apostrophe> <dead_psili> <Greek_omega>	: "ᾤ"	U1FA4 # GREEK SMALL LETTER OMEGA WITH PSILI AND OXIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <apostrophe> <parenright> <Greek_omega>	: "ᾤ"	U1FA4 # GREEK SMALL LETTER OMEGA WITH PSILI AND OXIA AND YPOGEGRAMMENI
<dead_iota> <dead_acute> <dead_dasia> <Greek_omega>	: "ᾥ"	U1FA5 # GREEK SMALL LETTER OMEGA WITH DASIA AND OXIA AND YPOGEGRAMMENI
<dead_iota> <dead_acute> <Multi_key> <parenleft> <Greek_omega>	: "ᾥ"	U1FA5 # GREEK SMALL LETTER OMEGA WITH DASIA AND OXIA AND YPOGEGRAMMENI
<dead_iota> <Multi_key> <apostrophe> <dead_dasia> <Greek_omega>	: "ᾥ"	U1FA5 # GREEK SMALL LETTER OMEGA WITH DASIA AND OXIA AND YPOGEGRAMMENI
<dead_iota> <Multi_key> <apostrophe> <parenleft> <Greek_omega>	: "ᾥ"	U1FA5 # GREEK SMALL LETTER OMEGA WITH DASIA AND OXIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <dead_acute> <dead_dasia> <Greek_omega>	: "ᾥ"	U1FA5 # GREEK SMALL LETTER OMEGA WITH DASIA AND OXIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <dead_acute> <parenleft> <Greek_omega>	: "ᾥ"	U1FA5 # GREEK SMALL LETTER OMEGA WITH DASIA AND OXIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <acute> <dead_dasia> <Greek_omega>	: "ᾥ"	U1FA5 # GREEK SMALL LETTER OMEGA WITH DASIA AND OXIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <acute> <parenleft> <Greek_omega>	: "ᾥ"	U1FA5 # GREEK SMALL LETTER OMEGA WITH DASIA AND OXIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <apostrophe> <dead_dasia> <Greek_omega>	: "ᾥ"	U1FA5 # GREEK SMALL LETTER OMEGA WITH DASIA AND OXIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <apostrophe> <parenleft> <Greek_omega>	: "ᾥ"	U1FA5 # GREEK SMALL LETTER OMEGA WITH DASIA AND OXIA AND YPOGEGRAMMENI
<dead_iota> <dead_tilde> <dead_psili> <Greek_omega>	: "ᾦ"	U1FA6 # GREEK SMALL LETTER OMEGA WITH PSILI AND PERISPOMENI AND YPOGEGRAMMENI
<dead_iota> <dead_tilde> <Multi_key> <parenright> <Greek_omega>	: "ᾦ"	U1FA6 # GREEK SMALL LETTER OMEGA WITH PSILI AND PERISPOMENI AND YPOGEGRAMMENI
<dead_iota> <Multi_key> <asciitilde> <dead_psili> <Greek_omega>	: "ᾦ"	U1FA6 # GREEK SMALL LETTER OMEGA WITH PSILI AND PERISPOMENI AND YPOGEGRAMMENI
<dead_iota> <Multi_key> <asciitilde> <parenright> <Greek_omega>	: "ᾦ"	U1FA6 # GREEK SMALL LETTER OMEGA WITH PSILI AND PERISPOMENI AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <dead_tilde> <dead_psili> <Greek_omega>	: "ᾦ"	U1FA6 # GREEK SMALL LETTER OMEGA WITH PSILI AND PERISPOMENI AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <dead_tilde> <parenright> <Greek_omega>	: "ᾦ"	U1FA6 # GREEK SMALL LETTER OMEGA WITH PSILI AND PERISPOMENI AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <asciitilde> <dead_psili> <Greek_omega>	: "ᾦ"	U1FA6 # GREEK SMALL LETTER OMEGA WITH PSILI AND PERISPOMENI AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <asciitilde> <parenright> <Greek_omega>	: "ᾦ"	U1FA6 # GREEK SMALL LETTER OMEGA WITH PSILI AND PERISPOMENI AND YPOGEGRAMMENI
<dead_iota> <dead_tilde> <dead_dasia> <Greek_omega>	: "ᾧ"	U1FA7 # GREEK SMALL LETTER OMEGA WITH DASIA AND PERISPOMENI AND YPOGEGRAMMENI
<dead_iota> <dead_tilde> <Multi_key> <parenleft> <Greek_omega>	: "ᾧ"	U1FA7 # GREEK SMALL LETTER OMEGA WITH DASIA AND PERISPOMENI AND YPOGEGRAMMENI
<dead_iota> <Multi_key> <asciitilde> <dead_dasia> <Greek_omega>	: "ᾧ"	U1FA7 # GREEK SMALL LETTER OMEGA WITH DASIA AND PERISPOMENI AND YPOGEGRAMMENI
<dead_iota> <Multi_key> <asciitilde> <parenleft> <Greek_omega>	: "ᾧ"	U1FA7 # GREEK SMALL LETTER OMEGA WITH DASIA AND PERISPOMENI AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <dead_tilde> <dead_dasia> <Greek_omega>	: "ᾧ"	U1FA7 # GREEK SMALL LETTER OMEGA WITH DASIA AND PERISPOMENI AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <dead_tilde> <parenleft> <Greek_omega>	: "ᾧ"	U1FA7 # GREEK SMALL LETTER OMEGA WITH DASIA AND PERISPOMENI AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <asciitilde> <dead_dasia> <Greek_omega>	: "ᾧ"	U1FA7 # GREEK SMALL LETTER OMEGA WITH DASIA AND PERISPOMENI AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <asciitilde> <parenleft> <Greek_omega>	: "ᾧ"	U1FA7 # GREEK SMALL LETTER OMEGA WITH DASIA AND PERISPOMENI AND YPOGEGRAMMENI
<dead_iota> <dead_psili> <Greek_OMEGA>	: "ᾨ"	U1FA8 # GREEK CAPITAL LETTER OMEGA WITH PSILI AND PROSGEGRAMMENI
<dead_iota> <Multi_key> <parenright> <Greek_OMEGA>	: "ᾨ"	U1FA8 # GREEK CAPITAL LETTER OMEGA WITH PSILI AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <dead_psili> <Greek_OMEGA>	: "ᾨ"	U1FA8 # GREEK CAPITAL LETTER OMEGA WITH PSILI AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <parenright> <Greek_OMEGA>	: "ᾨ"	U1FA8 # GREEK CAPITAL LETTER OMEGA WITH PSILI AND PROSGEGRAMMENI
<dead_iota> <dead_dasia> <Greek_OMEGA>	: "ᾩ"	U1FA9 # GREEK CAPITAL LETTER OMEGA WITH DASIA AND PROSGEGRAMMENI
<dead_iota> <Multi_key> <parenleft> <Greek_OMEGA>	: "ᾩ"	U1FA9 # GREEK CAPITAL LETTER OMEGA WITH DASIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <dead_dasia> <Greek_OMEGA>	: "ᾩ"	U1FA9 # GREEK CAPITAL LETTER OMEGA WITH DASIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <parenleft> <Greek_OMEGA>	: "ᾩ"	U1FA9 # GREEK CAPITAL LETTER OMEGA WITH DASIA AND PROSGEGRAMMENI
<dead_iota> <dead_grave> <dead_psili> <Greek_OMEGA>	: "ᾪ"	U1FAA # GREEK CAPITAL LETTER OMEGA WITH PSILI AND VARIA AND PROSGEGRAMMENI
<dead_iota> <dead_grave> <Multi_key> <parenright> <Greek_OMEGA>	: "ᾪ"	U1FAA # GREEK CAPITAL LETTER OMEGA WITH PSILI AND VARIA AND PROSGEGRAMMENI
<dead_iota> <Multi_key> <grave> <dead_psili> <Greek_OMEGA>	: "ᾪ"	U1FAA # GREEK CAPITAL LETTER OMEGA WITH PSILI AND VARIA AND PROSGEGRAMMENI
<dead_iota> <Multi_key> <grave> <parenright> <Greek_OMEGA>	: "ᾪ"	U1FAA # GREEK CAPITAL LETTER OMEGA WITH PSILI AND VARIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <dead_grave> <dead_psili> <Greek_OMEGA>	: "ᾪ"	U1FAA # GREEK CAPITAL LETTER OMEGA WITH PSILI AND VARIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <dead_grave> <parenright> <Greek_OMEGA>	: "ᾪ"	U1FAA # GREEK CAPITAL LETTER OMEGA WITH PSILI AND VARIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <grave> <dead_psili> <Greek_OMEGA>	: "ᾪ"	U1FAA # GREEK CAPITAL LETTER OMEGA WITH PSILI AND VARIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <grave> <parenright> <Greek_OMEGA>	: "ᾪ"	U1FAA # GREEK CAPITAL LETTER OMEGA WITH PSILI AND VARIA AND PROSGEGRAMMENI
<dead_iota> <dead_grave> <dead_dasia> <Greek_OMEGA>	: "ᾫ"	U1FAB # GREEK CAPITAL LETTER OMEGA WITH DASIA AND VARIA AND PROSGEGRAMMENI
<dead_iota> <dead_grave> <Multi_key> <parenleft> <Greek_OMEGA>	: "ᾫ"	U1FAB # GREEK CAPITAL LETTER OMEGA WITH DASIA AND VARIA AND PROSGEGRAMMENI
<dead_iota> <Multi_key> <grave> <dead_dasia> <Greek_OMEGA>	: "ᾫ"	U1FAB # GREEK CAPITAL LETTER OMEGA WITH DASIA AND VARIA AND PROSGEGRAMMENI
<dead_iota> <Multi_key> <grave> <parenleft> <Greek_OMEGA>	: "ᾫ"	U1FAB # GREEK CAPITAL LETTER OMEGA WITH DASIA AND VARIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <dead_grave> <dead_dasia> <Greek_OMEGA>	: "ᾫ"	U1FAB # GREEK CAPITAL LETTER OMEGA WITH DASIA AND VARIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <dead_grave> <parenleft> <Greek_OMEGA>	: "ᾫ"	U1FAB # GREEK CAPITAL LETTER OMEGA WITH DASIA AND VARIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <grave> <dead_dasia> <Greek_OMEGA>	: "ᾫ"	U1FAB # GREEK CAPITAL LETTER OMEGA WITH DASIA AND VARIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <grave> <parenleft> <Greek_OMEGA>	: "ᾫ"	U1FAB # GREEK CAPITAL LETTER OMEGA WITH DASIA AND VARIA AND PROSGEGRAMMENI
<dead_iota> <dead_acute> <dead_psili> <Greek_OMEGA>	: "ᾬ"	U1FAC # GREEK CAPITAL LETTER OMEGA WITH PSILI AND OXIA AND PROSGEGRAMMENI
<dead_iota> <dead_acute> <Multi_key> <parenright> <Greek_OMEGA>	: "ᾬ"	U1FAC # GREEK CAPITAL LETTER OMEGA WITH PSILI AND OXIA AND PROSGEGRAMMENI
<dead_iota> <Multi_key> <apostrophe> <dead_psili> <Greek_OMEGA>	: "ᾬ"	U1FAC # GREEK CAPITAL LETTER OMEGA WITH PSILI AND OXIA AND PROSGEGRAMMENI
<dead_iota> <Multi_key> <apostrophe> <parenright> <Greek_OMEGA>	: "ᾬ"	U1FAC # GREEK CAPITAL LETTER OMEGA WITH PSILI AND OXIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <dead_acute> <dead_psili> <Greek_OMEGA>	: "ᾬ"	U1FAC # GREEK CAPITAL LETTER OMEGA WITH PSILI AND OXIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <dead_acute> <parenright> <Greek_OMEGA>	: "ᾬ"	U1FAC # GREEK CAPITAL LETTER OMEGA WITH PSILI AND OXIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <acute> <dead_psili> <Greek_OMEGA>	: "ᾬ"	U1FAC # GREEK CAPITAL LETTER OMEGA WITH PSILI AND OXIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <acute> <parenright> <Greek_OMEGA>	: "ᾬ"	U1FAC # GREEK CAPITAL LETTER OMEGA WITH PSILI AND OXIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <apostrophe> <dead_psili> <Greek_OMEGA>	: "ᾬ"	U1FAC # GREEK CAPITAL LETTER OMEGA WITH PSILI AND OXIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <apostrophe> <parenright> <Greek_OMEGA>	: "ᾬ"	U1FAC # GREEK CAPITAL LETTER OMEGA WITH PSILI AND OXIA AND PROSGEGRAMMENI
<dead_iota> <dead_acute> <dead_dasia> <Greek_OMEGA>	: "ᾭ"	U1FAD # GREEK CAPITAL LETTER OMEGA WITH DASIA AND OXIA AND PROSGEGRAMMENI
<dead_iota> <dead_acute> <Multi_key> <parenleft> <Greek_OMEGA>	: "ᾭ"	U1FAD # GREEK CAPITAL LETTER OMEGA WITH DASIA AND OXIA AND PROSGEGRAMMENI
<dead_iota> <Multi_key> <apostrophe> <dead_dasia> <Greek_OMEGA>	: "ᾭ"	U1FAD # GREEK CAPITAL LETTER OMEGA WITH DASIA AND OXIA AND PROSGEGRAMMENI
<dead_iota> <Multi_key> <apostrophe> <parenleft> <Greek_OMEGA>	: "ᾭ"	U1FAD # GREEK CAPITAL LETTER OMEGA WITH DASIA AND OXIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <dead_acute> <dead_dasia> <Greek_OMEGA>	: "ᾭ"	U1FAD # GREEK CAPITAL LETTER OMEGA WITH DASIA AND OXIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <dead_acute> <parenleft> <Greek_OMEGA>	: "ᾭ"	U1FAD # GREEK CAPITAL LETTER OMEGA WITH DASIA AND OXIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <acute> <dead_dasia> <Greek_OMEGA>	: "ᾭ"	U1FAD # GREEK CAPITAL LETTER OMEGA WITH DASIA AND OXIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <acute> <parenleft> <Greek_OMEGA>	: "ᾭ"	U1FAD # GREEK CAPITAL LETTER OMEGA WITH DASIA AND OXIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <apostrophe> <dead_dasia> <Greek_OMEGA>	: "ᾭ"	U1FAD # GREEK CAPITAL LETTER OMEGA WITH DASIA AND OXIA AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <apostrophe> <parenleft> <Greek_OMEGA>	: "ᾭ"	U1FAD # GREEK CAPITAL LETTER OMEGA WITH DASIA AND OXIA AND PROSGEGRAMMENI
<dead_iota> <dead_tilde> <dead_psili> <Greek_OMEGA>	: "ᾮ"	U1FAE # GREEK CAPITAL LETTER OMEGA WITH PSILI AND PERISPOMENI AND PROSGEGRAMMENI
<dead_iota> <dead_tilde> <Multi_key> <parenright> <Greek_OMEGA>	: "ᾮ"	U1FAE # GREEK CAPITAL LETTER OMEGA WITH PSILI AND PERISPOMENI AND PROSGEGRAMMENI
<dead_iota> <Multi_key> <asciitilde> <dead_psili> <Greek_OMEGA>	: "ᾮ"	U1FAE # GREEK CAPITAL LETTER OMEGA WITH PSILI AND PERISPOMENI AND PROSGEGRAMMENI
<dead_iota> <Multi_key> <asciitilde> <parenright> <Greek_OMEGA>	: "ᾮ"	U1FAE # GREEK CAPITAL LETTER OMEGA WITH PSILI AND PERISPOMENI AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <dead_tilde> <dead_psili> <Greek_OMEGA>	: "ᾮ"	U1FAE # GREEK CAPITAL LETTER OMEGA WITH PSILI AND PERISPOMENI AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <dead_tilde> <parenright> <Greek_OMEGA>	: "ᾮ"	U1FAE # GREEK CAPITAL LETTER OMEGA WITH PSILI AND PERISPOMENI AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <asciitilde> <dead_psili> <Greek_OMEGA>	: "ᾮ"	U1FAE # GREEK CAPITAL LETTER OMEGA WITH PSILI AND PERISPOMENI AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <asciitilde> <parenright> <Greek_OMEGA>	: "ᾮ"	U1FAE # GREEK CAPITAL LETTER OMEGA WITH PSILI AND PERISPOMENI AND PROSGEGRAMMENI
<dead_iota> <dead_tilde> <dead_dasia> <Greek_OMEGA>	: "ᾯ"	U1FAF # GREEK CAPITAL LETTER OMEGA WITH DASIA AND PERISPOMENI AND PROSGEGRAMMENI
<dead_iota> <dead_tilde> <Multi_key> <parenleft> <Greek_OMEGA>	: "ᾯ"	U1FAF # GREEK CAPITAL LETTER OMEGA WITH DASIA AND PERISPOMENI AND PROSGEGRAMMENI
<dead_iota> <Multi_key> <asciitilde> <dead_dasia> <Greek_OMEGA>	: "ᾯ"	U1FAF # GREEK CAPITAL LETTER OMEGA WITH DASIA AND PERISPOMENI AND PROSGEGRAMMENI
<dead_iota> <Multi_key> <asciitilde> <parenleft> <Greek_OMEGA>	: "ᾯ"	U1FAF # GREEK CAPITAL LETTER OMEGA WITH DASIA AND PERISPOMENI AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <dead_tilde> <dead_dasia> <Greek_OMEGA>	: "ᾯ"	U1FAF # GREEK CAPITAL LETTER OMEGA WITH DASIA AND PERISPOMENI AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <dead_tilde> <parenleft> <Greek_OMEGA>	: "ᾯ"	U1FAF # GREEK CAPITAL LETTER OMEGA WITH DASIA AND PERISPOMENI AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <asciitilde> <dead_dasia> <Greek_OMEGA>	: "ᾯ"	U1FAF # GREEK CAPITAL LETTER OMEGA WITH DASIA AND PERISPOMENI AND PROSGEGRAMMENI
<Multi_key> <Greek_iota> <asciitilde> <parenleft> <Greek_OMEGA>	: "ᾯ"	U1FAF # GREEK CAPITAL LETTER OMEGA WITH DASIA AND PERISPOMENI AND PROSGEGRAMMENI
<dead_breve> <Greek_alpha>		: "ᾰ"	U1FB0 # GREEK SMALL LETTER ALPHA WITH VRACHY
<Multi_key> <U> <Greek_alpha>		: "ᾰ"	U1FB0 # GREEK SMALL LETTER ALPHA WITH VRACHY
<Multi_key> <b> <Greek_alpha>		: "ᾰ"	U1FB0 # GREEK SMALL LETTER ALPHA WITH VRACHY
<dead_macron> <Greek_alpha>		: "ᾱ"	U1FB1 # GREEK SMALL LETTER ALPHA WITH MACRON
<Multi_key> <macron> <Greek_alpha>	: "ᾱ"	U1FB1 # GREEK SMALL LETTER ALPHA WITH MACRON
<Multi_key> <underscore> <Greek_alpha>	: "ᾱ"	U1FB1 # GREEK SMALL LETTER ALPHA WITH MACRON
<dead_iota> <dead_grave> <Greek_alpha>	: "ᾲ"	U1FB2 # GREEK SMALL LETTER ALPHA WITH VARIA AND YPOGEGRAMMENI
<dead_iota> <Multi_key> <grave> <Greek_alpha>	: "ᾲ"	U1FB2 # GREEK SMALL LETTER ALPHA WITH VARIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <dead_grave> <Greek_alpha>	: "ᾲ"	U1FB2 # GREEK SMALL LETTER ALPHA WITH VARIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <grave> <Greek_alpha>	: "ᾲ"	U1FB2 # GREEK SMALL LETTER ALPHA WITH VARIA AND YPOGEGRAMMENI
<dead_iota> <Greek_alpha>		: "ᾳ"	U1FB3 # GREEK SMALL LETTER ALPHA WITH YPOGEGRAMMENI
<Multi_key> <Greek_iota> <Greek_alpha>	: "ᾳ"	U1FB3 # GREEK SMALL LETTER ALPHA WITH YPOGEGRAMMENI
<dead_iota> <dead_acute> <Greek_alpha>	: "ᾴ"	U1FB4 # GREEK SMALL LETTER ALPHA WITH OXIA AND YPOGEGRAMMENI
<dead_iota> <Multi_key> <apostrophe> <Greek_alpha>	: "ᾴ"	U1FB4 # GREEK SMALL LETTER ALPHA WITH OXIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <dead_acute> <Greek_alpha>	: "ᾴ"	U1FB4 # GREEK SMALL LETTER ALPHA WITH OXIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <acute> <Greek_alpha>	: "ᾴ"	U1FB4 # GREEK SMALL LETTER ALPHA WITH OXIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <apostrophe> <Greek_alpha>	: "ᾴ"	U1FB4 # GREEK SMALL LETTER ALPHA WITH OXIA AND YPOGEGRAMMENI
<dead_tilde> <Greek_alpha>		: "ᾶ"	U1FB6 # GREEK SMALL LETTER ALPHA WITH PERISPOMENI
<Multi_key> <asciitilde> <Greek_alpha>	: "ᾶ"	U1FB6 # GREEK SMALL LETTER ALPHA WITH PERISPOMENI
<dead_iota> <dead_tilde> <Greek_alpha>	: "ᾷ"	U1FB7 # GREEK SMALL LETTER ALPHA WITH PERISPOMENI AND YPOGEGRAMMENI
<dead_iota> <Multi_key> <asciitilde> <Greek_alpha>	: "ᾷ"	U1FB7 # GREEK SMALL LETTER ALPHA WITH PERISPOMENI AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <dead_tilde> <Greek_alpha>	: "ᾷ"	U1FB7 # GREEK SMALL LETTER ALPHA WITH PERISPOMENI AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <asciitilde> <Greek_alpha>	: "ᾷ"	U1FB7 # GREEK SMALL LETTER ALPHA WITH PERISPOMENI AND YPOGEGRAMMENI
<dead_breve> <Greek_ALPHA>		: "Ᾰ"	U1FB8 # GREEK CAPITAL LETTER ALPHA WITH VRACHY
<Multi_key> <U> <Greek_ALPHA>		: "Ᾰ"	U1FB8 # GREEK CAPITAL LETTER ALPHA WITH VRACHY
<Multi_key> <b> <Greek_ALPHA>		: "Ᾰ"	U1FB8 # GREEK CAPITAL LETTER ALPHA WITH VRACHY
<dead_macron> <Greek_ALPHA>		: "Ᾱ"	U1FB9 # GREEK CAPITAL LETTER ALPHA WITH MACRON
<Multi_key> <macron> <Greek_ALPHA>	: "Ᾱ"	U1FB9 # GREEK CAPITAL LETTER ALPHA WITH MACRON
<Multi_key> <underscore> <Greek_ALPHA>	: "Ᾱ"	U1FB9 # GREEK CAPITAL LETTER ALPHA WITH MACRON
<dead_grave> <Greek_ALPHA>		: "Ὰ"	U1FBA # GREEK CAPITAL LETTER ALPHA WITH VARIA
<Multi_key> <grave> <Greek_ALPHA>	: "Ὰ"	U1FBA # GREEK CAPITAL LETTER ALPHA WITH VARIA
<dead_iota> <Greek_ALPHA>		: "ᾼ"	U1FBC # GREEK CAPITAL LETTER ALPHA WITH PROSGEGRAMMENI
<Multi_key> <Greek_iota> <Greek_ALPHA>	: "ᾼ"	U1FBC # GREEK CAPITAL LETTER ALPHA WITH PROSGEGRAMMENI
<Multi_key> <diaeresis> <dead_tilde>	: "῁"	U1FC1 # GREEK DIALYTIKA AND PERISPOMENI
<Multi_key> <diaeresis> <asciitilde>	: "῁"	U1FC1 # GREEK DIALYTIKA AND PERISPOMENI
<dead_iota> <dead_grave> <Greek_eta>	: "ῂ"	U1FC2 # GREEK SMALL LETTER ETA WITH VARIA AND YPOGEGRAMMENI
<dead_iota> <Multi_key> <grave> <Greek_eta>	: "ῂ"	U1FC2 # GREEK SMALL LETTER ETA WITH VARIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <dead_grave> <Greek_eta>	: "ῂ"	U1FC2 # GREEK SMALL LETTER ETA WITH VARIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <grave> <Greek_eta>	: "ῂ"	U1FC2 # GREEK SMALL LETTER ETA WITH VARIA AND YPOGEGRAMMENI
<dead_iota> <Greek_eta>			: "ῃ"	U1FC3 # GREEK SMALL LETTER ETA WITH YPOGEGRAMMENI
<Multi_key> <Greek_iota> <Greek_eta>	: "ῃ"	U1FC3 # GREEK SMALL LETTER ETA WITH YPOGEGRAMMENI
<dead_iota> <dead_acute> <Greek_eta>	: "ῄ"	U1FC4 # GREEK SMALL LETTER ETA WITH OXIA AND YPOGEGRAMMENI
<dead_iota> <Multi_key> <apostrophe> <Greek_eta>	: "ῄ"	U1FC4 # GREEK SMALL LETTER ETA WITH OXIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <dead_acute> <Greek_eta>	: "ῄ"	U1FC4 # GREEK SMALL LETTER ETA WITH OXIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <acute> <Greek_eta>	: "ῄ"	U1FC4 # GREEK SMALL LETTER ETA WITH OXIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <apostrophe> <Greek_eta>	: "ῄ"	U1FC4 # GREEK SMALL LETTER ETA WITH OXIA AND YPOGEGRAMMENI
<dead_tilde> <Greek_eta>		: "ῆ"	U1FC6 # GREEK SMALL LETTER ETA WITH PERISPOMENI
<Multi_key> <asciitilde> <Greek_eta>	: "ῆ"	U1FC6 # GREEK SMALL LETTER ETA WITH PERISPOMENI
<dead_iota> <dead_tilde> <Greek_eta>	: "ῇ"	U1FC7 # GREEK SMALL LETTER ETA WITH PERISPOMENI AND YPOGEGRAMMENI
<dead_iota> <Multi_key> <asciitilde> <Greek_eta>	: "ῇ"	U1FC7 # GREEK SMALL LETTER ETA WITH PERISPOMENI AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <dead_tilde> <Greek_eta>	: "ῇ"	U1FC7 # GREEK SMALL LETTER ETA WITH PERISPOMENI AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <asciitilde> <Greek_eta>	: "ῇ"	U1FC7 # GREEK SMALL LETTER ETA WITH PERISPOMENI AND YPOGEGRAMMENI
<dead_grave> <Greek_EPSILON>		: "Ὲ"	U1FC8 # GREEK CAPITAL LETTER EPSILON WITH VARIA
<Multi_key> <grave> <Greek_EPSILON>	: "Ὲ"	U1FC8 # GREEK CAPITAL LETTER EPSILON WITH VARIA
<dead_grave> <Greek_ETA>		: "Ὴ"	U1FCA # GREEK CAPITAL LETTER ETA WITH VARIA
<Multi_key> <grave> <Greek_ETA>		: "Ὴ"	U1FCA # GREEK CAPITAL LETTER ETA WITH VARIA
<dead_iota> <Greek_ETA>			: "ῌ"	U1FCC # GREEK CAPITAL LETTER ETA WITH PROSGEGRAMMENI
<Multi_key> <Greek_iota> <Greek_ETA>	: "ῌ"	U1FCC # GREEK CAPITAL LETTER ETA WITH PROSGEGRAMMENI
<dead_breve> <Greek_iota>		: "ῐ"	U1FD0 # GREEK SMALL LETTER IOTA WITH VRACHY
<Multi_key> <U> <Greek_iota>		: "ῐ"	U1FD0 # GREEK SMALL LETTER IOTA WITH VRACHY
<Multi_key> <b> <Greek_iota>		: "ῐ"	U1FD0 # GREEK SMALL LETTER IOTA WITH VRACHY
<dead_macron> <Greek_iota>		: "ῑ"	U1FD1 # GREEK SMALL LETTER IOTA WITH MACRON
<Multi_key> <macron> <Greek_iota>	: "ῑ"	U1FD1 # GREEK SMALL LETTER IOTA WITH MACRON
<Multi_key> <underscore> <Greek_iota>	: "ῑ"	U1FD1 # GREEK SMALL LETTER IOTA WITH MACRON
<dead_grave> <dead_diaeresis> <Greek_iota>	: "ῒ"	U1FD2 # GREEK SMALL LETTER IOTA WITH DIALYTIKA AND VARIA
<dead_grave> <Multi_key> <quotedbl> <Greek_iota>	: "ῒ"	U1FD2 # GREEK SMALL LETTER IOTA WITH DIALYTIKA AND VARIA
<Multi_key> <grave> <dead_diaeresis> <Greek_iota>	: "ῒ"	U1FD2 # GREEK SMALL LETTER IOTA WITH DIALYTIKA AND VARIA
<Multi_key> <grave> <quotedbl> <Greek_iota>	: "ῒ"	U1FD2 # GREEK SMALL LETTER IOTA WITH DIALYTIKA AND VARIA
<dead_tilde> <Greek_iota>		: "ῖ"	U1FD6 # GREEK SMALL LETTER IOTA WITH PERISPOMENI
<Multi_key> <asciitilde> <Greek_iota>	: "ῖ"	U1FD6 # GREEK SMALL LETTER IOTA WITH PERISPOMENI
<dead_tilde> <dead_diaeresis> <Greek_iota>	: "ῗ"	U1FD7 # GREEK SMALL LETTER IOTA WITH DIALYTIKA AND PERISPOMENI
<dead_tilde> <Multi_key> <quotedbl> <Greek_iota>	: "ῗ"	U1FD7 # GREEK SMALL LETTER IOTA WITH DIALYTIKA AND PERISPOMENI
<Multi_key> <asciitilde> <dead_diaeresis> <Greek_iota>	: "ῗ"	U1FD7 # GREEK SMALL LETTER IOTA WITH DIALYTIKA AND PERISPOMENI
<Multi_key> <asciitilde> <quotedbl> <Greek_iota>	: "ῗ"	U1FD7 # GREEK SMALL LETTER IOTA WITH DIALYTIKA AND PERISPOMENI
<dead_breve> <Greek_IOTA>		: "Ῐ"	U1FD8 # GREEK CAPITAL LETTER IOTA WITH VRACHY
<Multi_key> <U> <Greek_IOTA>		: "Ῐ"	U1FD8 # GREEK CAPITAL LETTER IOTA WITH VRACHY
<Multi_key> <b> <Greek_IOTA>		: "Ῐ"	U1FD8 # GREEK CAPITAL LETTER IOTA WITH VRACHY
<dead_macron> <Greek_IOTA>		: "Ῑ"	U1FD9 # GREEK CAPITAL LETTER IOTA WITH MACRON
<Multi_key> <macron> <Greek_IOTA>	: "Ῑ"	U1FD9 # GREEK CAPITAL LETTER IOTA WITH MACRON
<Multi_key> <underscore> <Greek_IOTA>	: "Ῑ"	U1FD9 # GREEK CAPITAL LETTER IOTA WITH MACRON
<dead_grave> <Greek_IOTA>		: "Ὶ"	U1FDA # GREEK CAPITAL LETTER IOTA WITH VARIA
<Multi_key> <grave> <Greek_IOTA>	: "Ὶ"	U1FDA # GREEK CAPITAL LETTER IOTA WITH VARIA
<dead_breve> <Greek_upsilon>		: "ῠ"	U1FE0 # GREEK SMALL LETTER UPSILON WITH VRACHY
<Multi_key> <U> <Greek_upsilon>		: "ῠ"	U1FE0 # GREEK SMALL LETTER UPSILON WITH VRACHY
<Multi_key> <b> <Greek_upsilon>		: "ῠ"	U1FE0 # GREEK SMALL LETTER UPSILON WITH VRACHY
<dead_macron> <Greek_upsilon>		: "ῡ"	U1FE1 # GREEK SMALL LETTER UPSILON WITH MACRON
<Multi_key> <macron> <Greek_upsilon>	: "ῡ"	U1FE1 # GREEK SMALL LETTER UPSILON WITH MACRON
<Multi_key> <underscore> <Greek_upsilon>	: "ῡ"	U1FE1 # GREEK SMALL LETTER UPSILON WITH MACRON
<dead_grave> <dead_diaeresis> <Greek_upsilon>	: "ῢ"	U1FE2 # GREEK SMALL LETTER UPSILON WITH DIALYTIKA AND VARIA
<dead_grave> <Multi_key> <quotedbl> <Greek_upsilon>	: "ῢ"	U1FE2 # GREEK SMALL LETTER UPSILON WITH DIALYTIKA AND VARIA
<Multi_key> <grave> <dead_diaeresis> <Greek_upsilon>	: "ῢ"	U1FE2 # GREEK SMALL LETTER UPSILON WITH DIALYTIKA AND VARIA
<Multi_key> <grave> <quotedbl> <Greek_upsilon>	: "ῢ"	U1FE2 # GREEK SMALL LETTER UPSILON WITH DIALYTIKA AND VARIA
<dead_psili> <Greek_rho>		: "ῤ"	U1FE4 # GREEK SMALL LETTER RHO WITH PSILI
<Multi_key> <parenright> <Greek_rho>	: "ῤ"	U1FE4 # GREEK SMALL LETTER RHO WITH PSILI
<dead_dasia> <Greek_rho>		: "ῥ"	U1FE5 # GREEK SMALL LETTER RHO WITH DASIA
<Multi_key> <parenleft> <Greek_rho>	: "ῥ"	U1FE5 # GREEK SMALL LETTER RHO WITH DASIA
<dead_tilde> <Greek_upsilon>		: "ῦ"	U1FE6 # GREEK SMALL LETTER UPSILON WITH PERISPOMENI
<Multi_key> <asciitilde> <Greek_upsilon>	: "ῦ"	U1FE6 # GREEK SMALL LETTER UPSILON WITH PERISPOMENI
<dead_tilde> <dead_diaeresis> <Greek_upsilon>	: "ῧ"	U1FE7 # GREEK SMALL LETTER UPSILON WITH DIALYTIKA AND PERISPOMENI
<dead_tilde> <Multi_key> <quotedbl> <Greek_upsilon>	: "ῧ"	U1FE7 # GREEK SMALL LETTER UPSILON WITH DIALYTIKA AND PERISPOMENI
<Multi_key> <asciitilde> <dead_diaeresis> <Greek_upsilon>	: "ῧ"	U1FE7 # GREEK SMALL LETTER UPSILON WITH DIALYTIKA AND PERISPOMENI
<Multi_key> <asciitilde> <quotedbl> <Greek_upsilon>	: "ῧ"	U1FE7 # GREEK SMALL LETTER UPSILON WITH DIALYTIKA AND PERISPOMENI
<dead_breve> <Greek_UPSILON>		: "Ῠ"	U1FE8 # GREEK CAPITAL LETTER UPSILON WITH VRACHY
<Multi_key> <U> <Greek_UPSILON>		: "Ῠ"	U1FE8 # GREEK CAPITAL LETTER UPSILON WITH VRACHY
<Multi_key> <b> <Greek_UPSILON>		: "Ῠ"	U1FE8 # GREEK CAPITAL LETTER UPSILON WITH VRACHY
<dead_macron> <Greek_UPSILON>		: "Ῡ"	U1FE9 # GREEK CAPITAL LETTER UPSILON WITH MACRON
<Multi_key> <macron> <Greek_UPSILON>	: "Ῡ"	U1FE9 # GREEK CAPITAL LETTER UPSILON WITH MACRON
<Multi_key> <underscore> <Greek_UPSILON>	: "Ῡ"	U1FE9 # GREEK CAPITAL LETTER UPSILON WITH MACRON
<dead_grave> <Greek_UPSILON>		: "Ὺ"	U1FEA # GREEK CAPITAL LETTER UPSILON WITH VARIA
<Multi_key> <grave> <Greek_UPSILON>	: "Ὺ"	U1FEA # GREEK CAPITAL LETTER UPSILON WITH VARIA
<dead_dasia> <Greek_RHO>		: "Ῥ"	U1FEC # GREEK CAPITAL LETTER RHO WITH DASIA
<Multi_key> <parenleft> <Greek_RHO>	: "Ῥ"	U1FEC # GREEK CAPITAL LETTER RHO WITH DASIA
<Multi_key> <diaeresis> <dead_grave>	: "῭"	U1FED # GREEK DIALYTIKA AND VARIA
<Multi_key> <diaeresis> <grave>		: "῭"	U1FED # GREEK DIALYTIKA AND VARIA
<dead_iota> <dead_grave> <Greek_omega>	: "ῲ"	U1FF2 # GREEK SMALL LETTER OMEGA WITH VARIA AND YPOGEGRAMMENI
<dead_iota> <Multi_key> <grave> <Greek_omega>	: "ῲ"	U1FF2 # GREEK SMALL LETTER OMEGA WITH VARIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <dead_grave> <Greek_omega>	: "ῲ"	U1FF2 # GREEK SMALL LETTER OMEGA WITH VARIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <grave> <Greek_omega>	: "ῲ"	U1FF2 # GREEK SMALL LETTER OMEGA WITH VARIA AND YPOGEGRAMMENI
<dead_iota> <Greek_omega>		: "ῳ"	U1FF3 # GREEK SMALL LETTER OMEGA WITH YPOGEGRAMMENI
<Multi_key> <Greek_iota> <Greek_omega>	: "ῳ"	U1FF3 # GREEK SMALL LETTER OMEGA WITH YPOGEGRAMMENI
<dead_iota> <dead_acute> <Greek_omega>	: "ῴ"	U1FF4 # GREEK SMALL LETTER OMEGA WITH OXIA AND YPOGEGRAMMENI
<dead_iota> <Multi_key> <apostrophe> <Greek_omega>	: "ῴ"	U1FF4 # GREEK SMALL LETTER OMEGA WITH OXIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <dead_acute> <Greek_omega>	: "ῴ"	U1FF4 # GREEK SMALL LETTER OMEGA WITH OXIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <acute> <Greek_omega>	: "ῴ"	U1FF4 # GREEK SMALL LETTER OMEGA WITH OXIA AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <apostrophe> <Greek_omega>	: "ῴ"	U1FF4 # GREEK SMALL LETTER OMEGA WITH OXIA AND YPOGEGRAMMENI
<dead_tilde> <Greek_omega>		: "ῶ"	U1FF6 # GREEK SMALL LETTER OMEGA WITH PERISPOMENI
<Multi_key> <asciitilde> <Greek_omega>	: "ῶ"	U1FF6 # GREEK SMALL LETTER OMEGA WITH PERISPOMENI
<dead_iota> <dead_tilde> <Greek_omega>	: "ῷ"	U1FF7 # GREEK SMALL LETTER OMEGA WITH PERISPOMENI AND YPOGEGRAMMENI
<dead_iota> <Multi_key> <asciitilde> <Greek_omega>	: "ῷ"	U1FF7 # GREEK SMALL LETTER OMEGA WITH PERISPOMENI AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <dead_tilde> <Greek_omega>	: "ῷ"	U1FF7 # GREEK SMALL LETTER OMEGA WITH PERISPOMENI AND YPOGEGRAMMENI
<Multi_key> <Greek_iota> <asciitilde> <Greek_omega>	: "ῷ"	U1FF7 # GREEK SMALL LETTER OMEGA WITH PERISPOMENI AND YPOGEGRAMMENI
<dead_grave> <Greek_OMICRON>		: "Ὸ"	U1FF8 # GREEK CAPITAL LETTER OMICRON WITH VARIA
<Multi_key> <grave> <Greek_OMICRON>	: "Ὸ"	U1FF8 # GREEK CAPITAL LETTER OMICRON WITH VARIA
<dead_grave> <Greek_OMEGA>		: "Ὼ"	U1FFA # GREEK CAPITAL LETTER OMEGA WITH VARIA
<Multi_key> <grave> <Greek_OMEGA>	: "Ὼ"	U1FFA # GREEK CAPITAL LETTER OMEGA WITH VARIA
<dead_iota> <Greek_OMEGA>		: "ῼ"	U1FFC # GREEK CAPITAL LETTER OMEGA WITH PROSGEGRAMMENI
<Multi_key> <Greek_iota> <Greek_OMEGA>	: "ῼ"	U1FFC # GREEK CAPITAL LETTER OMEGA WITH PROSGEGRAMMENI
# Superscripts and Subscripts
<dead_circumflex> <0>				: "⁰"	U2070 # SUPERSCRIPT ZERO
<Multi_key> <asciicircum> <0>			: "⁰"	U2070 # SUPERSCRIPT ZERO
<dead_circumflex> <KP_0>			: "⁰"	U2070 # SUPERSCRIPT ZERO
<Multi_key> <asciicircum> <KP_0>		: "⁰"	U2070 # SUPERSCRIPT ZERO
<dead_circumflex> <Multi_key> <underscore> <i>	: "ⁱ"	U2071 # SUPERSCRIPT LATIN SMALL LETTER I
<Multi_key> <asciicircum> <underscore> <i>	: "ⁱ"	U2071 # SUPERSCRIPT LATIN SMALL LETTER I
<dead_circumflex> <4>				: "⁴"	U2074 # SUPERSCRIPT FOUR
<Multi_key> <asciicircum> <4>			: "⁴"	U2074 # SUPERSCRIPT FOUR
<dead_circumflex> <KP_4>			: "⁴"	U2074 # SUPERSCRIPT FOUR
<Multi_key> <asciicircum> <KP_4>		: "⁴"	U2074 # SUPERSCRIPT FOUR
<dead_circumflex> <5>				: "⁵"	U2075 # SUPERSCRIPT FIVE
<Multi_key> <asciicircum> <5>			: "⁵"	U2075 # SUPERSCRIPT FIVE
<dead_circumflex> <KP_5>			: "⁵"	U2075 # SUPERSCRIPT FIVE
<Multi_key> <asciicircum> <KP_5>		: "⁵"	U2075 # SUPERSCRIPT FIVE
<dead_circumflex> <6>				: "⁶"	U2076 # SUPERSCRIPT SIX
<Multi_key> <asciicircum> <6>			: "⁶"	U2076 # SUPERSCRIPT SIX
<dead_circumflex> <KP_6>			: "⁶"	U2076 # SUPERSCRIPT SIX
<Multi_key> <asciicircum> <KP_6>		: "⁶"	U2076 # SUPERSCRIPT SIX
<dead_circumflex> <7>				: "⁷"	U2077 # SUPERSCRIPT SEVEN
<Multi_key> <asciicircum> <7>			: "⁷"	U2077 # SUPERSCRIPT SEVEN
<dead_circumflex> <KP_7>			: "⁷"	U2077 # SUPERSCRIPT SEVEN
<Multi_key> <asciicircum> <KP_7>		: "⁷"	U2077 # SUPERSCRIPT SEVEN
<dead_circumflex> <8>				: "⁸"	U2078 # SUPERSCRIPT EIGHT
<Multi_key> <asciicircum> <8>			: "⁸"	U2078 # SUPERSCRIPT EIGHT
<dead_circumflex> <KP_8>			: "⁸"	U2078 # SUPERSCRIPT EIGHT
<Multi_key> <asciicircum> <KP_8>		: "⁸"	U2078 # SUPERSCRIPT EIGHT
<dead_circumflex> <9>				: "⁹"	U2079 # SUPERSCRIPT NINE
<Multi_key> <asciicircum> <9>			: "⁹"	U2079 # SUPERSCRIPT NINE
<dead_circumflex> <KP_9>			: "⁹"	U2079 # SUPERSCRIPT NINE
<Multi_key> <asciicircum> <KP_9>		: "⁹"	U2079 # SUPERSCRIPT NINE
<dead_circumflex> <plus>			: "⁺"	U207A # SUPERSCRIPT PLUS SIGN
<Multi_key> <asciicircum> <plus>		: "⁺"	U207A # SUPERSCRIPT PLUS SIGN
<dead_circumflex> <KP_Add>			: "⁺"	U207A # SUPERSCRIPT PLUS SIGN
<Multi_key> <asciicircum> <KP_Add>		: "⁺"	U207A # SUPERSCRIPT PLUS SIGN
<dead_circumflex> <minus>			: "⁻"	U207B # SUPERSCRIPT MINUS
<Multi_key> <asciicircum> <minus>		: "⁻"	U207B # SUPERSCRIPT MINUS
<dead_circumflex> <U2212>			: "⁻"	U207B # SUPERSCRIPT MINUS
<Multi_key> <asciicircum> <U2212>		: "⁻"	U207B # SUPERSCRIPT MINUS
<dead_circumflex> <equal>			: "⁼"	U207C # SUPERSCRIPT EQUALS SIGN
<Multi_key> <asciicircum> <equal>		: "⁼"	U207C # SUPERSCRIPT EQUALS SIGN
<dead_circumflex> <KP_Equal>			: "⁼"	U207C # SUPERSCRIPT EQUALS SIGN
<Multi_key> <asciicircum> <KP_Equal>		: "⁼"	U207C # SUPERSCRIPT EQUALS SIGN
<dead_circumflex> <parenleft>			: "⁽"	U207D # SUPERSCRIPT LEFT PARENTHESIS
<Multi_key> <asciicircum> <parenleft>		: "⁽"	U207D # SUPERSCRIPT LEFT PARENTHESIS
<dead_circumflex> <parenright>			: "⁾"	U207E # SUPERSCRIPT RIGHT PARENTHESIS
<Multi_key> <asciicircum> <parenright>		: "⁾"	U207E # SUPERSCRIPT RIGHT PARENTHESIS
<dead_circumflex> <Multi_key> <underscore> <n>	: "ⁿ"	U207F # SUPERSCRIPT LATIN SMALL LETTER N
<Multi_key> <asciicircum> <underscore> <n>	: "ⁿ"	U207F # SUPERSCRIPT LATIN SMALL LETTER N
<dead_caron> <0>				: "₀"	U2080 # SUBSCRIPT ZERO
<Multi_key> <underscore> <0>			: "₀"	U2080 # SUBSCRIPT ZERO
<Multi_key> <underscore> <KP_0>			: "₀"	U2080 # SUBSCRIPT ZERO
<dead_caron> <1>				: "₁"	U2081 # SUBSCRIPT ONE
<Multi_key> <underscore> <1>			: "₁"	U2081 # SUBSCRIPT ONE
<Multi_key> <underscore> <KP_1>			: "₁"	U2081 # SUBSCRIPT ONE
<dead_caron> <2>				: "₂"	U2082 # SUBSCRIPT TWO
<Multi_key> <underscore> <2>			: "₂"	U2082 # SUBSCRIPT TWO
<Multi_key> <underscore> <KP_2>			: "₂"	U2082 # SUBSCRIPT TWO
<dead_caron> <3>				: "₃"	U2083 # SUBSCRIPT THREE
<Multi_key> <underscore> <3>			: "₃"	U2083 # SUBSCRIPT THREE
<Multi_key> <underscore> <KP_3>			: "₃"	U2083 # SUBSCRIPT THREE
<dead_caron> <4>				: "₄"	U2084 # SUBSCRIPT FOUR
<Multi_key> <underscore> <4>			: "₄"	U2084 # SUBSCRIPT FOUR
<Multi_key> <underscore> <KP_4>			: "₄"	U2084 # SUBSCRIPT FOUR
<dead_caron> <5>				: "₅"	U2085 # SUBSCRIPT FIVE
<Multi_key> <underscore> <5>			: "₅"	U2085 # SUBSCRIPT FIVE
<Multi_key> <underscore> <KP_5>			: "₅"	U2085 # SUBSCRIPT FIVE
<dead_caron> <6>				: "₆"	U2086 # SUBSCRIPT SIX
<Multi_key> <underscore> <6>			: "₆"	U2086 # SUBSCRIPT SIX
<Multi_key> <underscore> <KP_6>			: "₆"	U2086 # SUBSCRIPT SIX
<dead_caron> <7>				: "₇"	U2087 # SUBSCRIPT SEVEN
<Multi_key> <underscore> <7>			: "₇"	U2087 # SUBSCRIPT SEVEN
<Multi_key> <underscore> <KP_7>			: "₇"	U2087 # SUBSCRIPT SEVEN
<dead_caron> <8>				: "₈"	U2088 # SUBSCRIPT EIGHT
<Multi_key> <underscore> <8>			: "₈"	U2088 # SUBSCRIPT EIGHT
<Multi_key> <underscore> <KP_8>			: "₈"	U2088 # SUBSCRIPT EIGHT
<dead_caron> <9>				: "₉"	U2089 # SUBSCRIPT NINE
<Multi_key> <underscore> <9>			: "₉"	U2089 # SUBSCRIPT NINE
<Multi_key> <underscore> <KP_9>			: "₉"	U2089 # SUBSCRIPT NINE
<dead_caron> <plus>				: "₊"	U208A # SUBSCRIPT PLUS SIGN
<Multi_key> <underscore> <plus>			: "₊"	U208A # SUBSCRIPT PLUS SIGN
<Multi_key> <underscore> <KP_Add>		: "₊"	U208A # SUBSCRIPT PLUS SIGN
<dead_caron> <minus>				: "₋"	U208B # SUBSCRIPT MINUS
<Multi_key> <underscore> <minus>		: "₋"	U208B # SUBSCRIPT MINUS
<Multi_key> <underscore> <U2212>		: "₋"	U208B # SUBSCRIPT MINUS
<dead_caron> <equal>				: "₌"	U208C # SUBSCRIPT EQUALS SIGN
<Multi_key> <underscore> <equal>		: "₌"	U208C # SUBSCRIPT EQUALS SIGN
<Multi_key> <underscore> <KP_Equal>		: "₌"	U208C # SUBSCRIPT EQUALS SIGN
<dead_caron> <parenleft>			: "₍"	U208D # SUBSCRIPT LEFT PARENTHESIS
<Multi_key> <underscore> <parenleft>		: "₍"	U208D # SUBSCRIPT LEFT PARENTHESIS
<dead_caron> <parenright>			: "₎"	U208E # SUBSCRIPT RIGHT PARENTHESIS
<Multi_key> <underscore> <parenright>		: "₎"	U208E # SUBSCRIPT RIGHT PARENTHESIS
# Letterlike Symbols
<Multi_key> <C> <C>			: "ℂ"	U2102 # DOUBLE-STRUCK CAPITAL C
<Multi_key> <N> <N>			: "ℕ"	U2115 # DOUBLE-STRUCK CAPITAL N
<Multi_key> <Q> <Q>			: "ℚ"	U211A # DOUBLE-STRUCK CAPITAL Q
<Multi_key> <R> <R>			: "ℝ"	U211D # DOUBLE-STRUCK CAPITAL R
<Multi_key> <Z> <Z>			: "ℤ"	U2124 # DOUBLE-STRUCK CAPITAL Z
<dead_circumflex> <Multi_key> <S> <M>	: "℠"	U2120 # SERVICE MARK
<Multi_key> <S> <M>			: "℠"	U2120 # SERVICE MARK
<dead_circumflex> <Multi_key> <s> <m>	: "℠"	U2120 # SERVICE MARK
<Multi_key> <s> <m>			: "℠"	U2120 # SERVICE MARK
<dead_circumflex> <Multi_key> <T> <M>	: "™"	U2122 # TRADE MARK SIGN
<Multi_key> <T> <M>			: "™"	U2122 # TRADE MARK SIGN
<dead_circumflex> <Multi_key> <t> <m>	: "™"	U2122 # TRADE MARK SIGN
<Multi_key> <t> <m>			: "™"	U2122 # TRADE MARK SIGN
# Number Forms
<Multi_key> <1> <7>			: "⅐"	U2150 # VULGAR FRACTION ONE SEVENTH
<Multi_key> <1> <9>			: "⅑"	U2151 # VULGAR FRACTION ONE NINTH
<Multi_key> <1> <1> <0>			: "⅒"	U2152 # VULGAR FRACTION ONE TENTH
<Multi_key> <1> <3>			: "⅓"	U2153 # VULGAR FRACTION ONE THIRD
<Multi_key> <2> <3>			: "⅔"	U2154 # VULGAR FRACTION TWO THIRDS
<Multi_key> <1> <5>			: "⅕"	U2155 # VULGAR FRACTION ONE FIFTH
<Multi_key> <2> <5>			: "⅖"	U2156 # VULGAR FRACTION TWO FIFTHS
<Multi_key> <3> <5>			: "⅗"	U2157 # VULGAR FRACTION THREE FIFTHS
<Multi_key> <4> <5>			: "⅘"	U2158 # VULGAR FRACTION FOUR FIFTHS
<Multi_key> <1> <6>			: "⅙"	U2159 # VULGAR FRACTION ONE SIXTH
<Multi_key> <5> <6>			: "⅚"	U215A # VULGAR FRACTION FIVE SIXTHS
<Multi_key> <1> <8>			: "⅛"	U215B # VULGAR FRACTION ONE EIGHTH
<Multi_key> <3> <8>			: "⅜"	U215C # VULGAR FRACTION THREE EIGHTHS
<Multi_key> <5> <8>			: "⅝"	U215D # VULGAR FRACTION FIVE EIGHTHS
<Multi_key> <7> <8>			: "⅞"	U215E # VULGAR FRACTION SEVEN EIGHTHS
<Multi_key> <0> <3>			: "↉"	U2189 # VULGAR FRACTION ZERO THIRDS
# Arrows
<Multi_key> <slash> <leftarrow>		: "↚"	U219A # LEFTWARDS ARROW WITH STROKE
<Multi_key> <KP_Divide> <leftarrow>	: "↚"	U219A # LEFTWARDS ARROW WITH STROKE
<Multi_key> <slash> <rightarrow>	: "↛"	U219B # RIGHTWARDS ARROW WITH STROKE
<Multi_key> <KP_Divide> <rightarrow>	: "↛"	U219B # RIGHTWARDS ARROW WITH STROKE
<Multi_key> <slash> <U2194>		: "↮"	U21AE # LEFT RIGHT ARROW WITH STROKE
<Multi_key> <KP_Divide> <U2194>		: "↮"	U21AE # LEFT RIGHT ARROW WITH STROKE
<Multi_key> <less> <minus>		: "←"	U2190 # LEFTWARDS ARROW
<Multi_key> <bar> <dead_circumflex>	: "↑"	U2191 # UPWARDS ARROW
<Multi_key> <dead_circumflex> <bar>	: "↑"	U2191 # UPWARDS ARROW
<Multi_key> <bar> <asciicircum>		: "↑"	U2191 # UPWARDS ARROW
<Multi_key> <asciicircum> <bar>		: "↑"	U2191 # UPWARDS ARROW
<Multi_key> <minus> <greater>		: "→"	U2192 # RIGHTWARDS ARROW
<Multi_key> <bar> <v>			: "↓"	U2193 # DOWNWARDS ARROW
<Multi_key> <v> <bar>			: "↓"	U2193 # DOWNWARDS ARROW
<Multi_key> <equal> <less>		: "⇐"	U21D0 # LEFTWARDS DOUBLE ARROW
<Multi_key> <equal> <asciicircum>	: "⇑"	U21D1 # UPWARDS DOUBLE ARROW
<Multi_key> <equal> <greater>		: "⇒"	U21D2 # RIGHTWARDS DOUBLE ARROW
<Multi_key> <equal> <v>			: "⇓"	U21D3 # DOWNWARDS DOUBLE ARROW
# Mathematical Operators
<Multi_key> <U2203> <slash>		: "∄"	U2204 # THERE DOES NOT EXIST
<Multi_key> <braceleft> <braceright>	: "∅"	U2205 # EMPTY SET
<Multi_key> <U2208> <slash>		: "∉"	U2209 # NOT AN ELEMENT OF
<Multi_key> <U220B> <slash>		: "∌"	U220C # DOES NOT CONTAIN AS MEMBER
<Multi_key> <minus> <underscore>	: "−"	U2212 # MINUS SIGN
<Multi_key> <U2223> <slash>		: "∤"	U2224 # DOES NOT DIVIDE
<Multi_key> <U2225> <slash>		: "∦"	U2226 # NOT PARALLEL TO
<Multi_key> <U223C> <slash>		: "≁"	U2241 # NOT TILDE
<Multi_key> <U2243> <slash>		: "≄"	U2244 # NOT ASYMPTOTICALLY EQUAL TO
<Multi_key> <approximate> <slash>	: "≇"	U2247 # NEITHER APPROXIMATELY NOR ACTUALLY EQUAL TO
<Multi_key> <U2248> <slash>		: "≉"	U2249 # NOT ALMOST EQUAL TO
<Multi_key> <slash> <equal>		: "≠"	U2260 # NOT EQUAL TO
<Multi_key> <equal> <slash>		: "≠"	U2260 # NOT EQUAL TO
<Multi_key> <KP_Equal> <slash>		: "≠"	U2260 # NOT EQUAL TO
<Multi_key> <identical> <slash>		: "≢"	U2262 # NOT IDENTICAL TO
<Multi_key> <less> <equal>		: "≤"	U2264 # LESS-THAN OR EQUAL TO
<Multi_key> <greater> <equal>		: "≥"	U2265 # GREATER-THAN OR EQUAL TO
<Multi_key> <U224D> <slash>		: "≭"	U226D # NOT EQUIVALENT TO
<Multi_key> <less> <slash>		: "≮"	U226E # NOT LESS-THAN
<Multi_key> <greater> <slash>		: "≯"	U226F # NOT GREATER-THAN
<Multi_key> <lessthanequal> <slash>	: "≰"	U2270 # NEITHER LESS-THAN NOR EQUAL TO
<Multi_key> <greaterthanequal> <slash>	: "≱"	U2271 # NEITHER GREATER-THAN NOR EQUAL TO
<Multi_key> <U2272> <slash>		: "≴"	U2274 # NEITHER LESS-THAN NOR EQUIVALENT TO
<Multi_key> <U2273> <slash>		: "≵"	U2275 # NEITHER GREATER-THAN NOR EQUIVALENT TO
<Multi_key> <U2276> <slash>		: "≸"	U2278 # NEITHER LESS-THAN NOR GREATER-THAN
<Multi_key> <U2277> <slash>		: "≹"	U2279 # NEITHER GREATER-THAN NOR LESS-THAN
<Multi_key> <U227A> <slash>		: "⊀"	U2280 # DOES NOT PRECEDE
<Multi_key> <U227B> <slash>		: "⊁"	U2281 # DOES NOT SUCCEED
<Multi_key> <includedin> <slash>	: "⊄"	U2284 # NOT A SUBSET OF
<Multi_key> <includes> <slash>		: "⊅"	U2285 # NOT A SUPERSET OF
<Multi_key> <U2286> <slash>		: "⊈"	U2288 # NEITHER A SUBSET OF NOR EQUAL TO
<Multi_key> <U2287> <slash>		: "⊉"	U2289 # NEITHER A SUPERSET OF NOR EQUAL TO
<Multi_key> <righttack> <slash>		: "⊬"	U22AC # DOES NOT PROVE
<Multi_key> <U22A8> <slash>		: "⊭"	U22AD # NOT TRUE
<Multi_key> <U22A9> <slash>		: "⊮"	U22AE # DOES NOT FORCE
<Multi_key> <U22AB> <slash>		: "⊯"	U22AF # NEGATED DOUBLE VERTICAL BAR DOUBLE RIGHT TURNSTILE
<Multi_key> <U227C> <slash>		: "⋠"	U22E0 # DOES NOT PRECEDE OR EQUAL
<Multi_key> <U227D> <slash>		: "⋡"	U22E1 # DOES NOT SUCCEED OR EQUAL
<Multi_key> <U2291> <slash>		: "⋢"	U22E2 # NOT SQUARE IMAGE OF OR EQUAL TO
<Multi_key> <U2292> <slash>		: "⋣"	U22E3 # NOT SQUARE ORIGINAL OF OR EQUAL TO
<Multi_key> <U22B2> <slash>		: "⋪"	U22EA # NOT NORMAL SUBGROUP OF
<Multi_key> <U22B3> <slash>		: "⋫"	U22EB # DOES NOT CONTAIN AS NORMAL SUBGROUP
<Multi_key> <U22B4> <slash>		: "⋬"	U22EC # NOT NORMAL SUBGROUP OF OR EQUAL TO
<Multi_key> <U22B5> <slash>		: "⋭"	U22ED # DOES NOT CONTAIN AS NORMAL SUBGROUP OR EQUAL
<Multi_key> <d> <i>			: "⌀"	U2300 # DIAMETER SIGN
# Enclosed Alphanumerics
<Multi_key> <parenleft> <1> <parenright>		: "①"	U2460 # CIRCLED DIGIT ONE
<Multi_key> <parenleft> <KP_1> <parenright>		: "①"	U2460 # CIRCLED DIGIT ONE
<Multi_key> <parenleft> <2> <parenright>		: "②"	U2461 # CIRCLED DIGIT TWO
<Multi_key> <parenleft> <KP_2> <parenright>		: "②"	U2461 # CIRCLED DIGIT TWO
<Multi_key> <parenleft> <3> <parenright>		: "③"	U2462 # CIRCLED DIGIT THREE
<Multi_key> <parenleft> <KP_3> <parenright>		: "③"	U2462 # CIRCLED DIGIT THREE
<Multi_key> <parenleft> <4> <parenright>		: "④"	U2463 # CIRCLED DIGIT FOUR
<Multi_key> <parenleft> <KP_4> <parenright>		: "④"	U2463 # CIRCLED DIGIT FOUR
<Multi_key> <parenleft> <5> <parenright>		: "⑤"	U2464 # CIRCLED DIGIT FIVE
<Multi_key> <parenleft> <KP_5> <parenright>		: "⑤"	U2464 # CIRCLED DIGIT FIVE
<Multi_key> <parenleft> <6> <parenright>		: "⑥"	U2465 # CIRCLED DIGIT SIX
<Multi_key> <parenleft> <KP_6> <parenright>		: "⑥"	U2465 # CIRCLED DIGIT SIX
<Multi_key> <parenleft> <7> <parenright>		: "⑦"	U2466 # CIRCLED DIGIT SEVEN
<Multi_key> <parenleft> <KP_7> <parenright>		: "⑦"	U2466 # CIRCLED DIGIT SEVEN
<Multi_key> <parenleft> <8> <parenright>		: "⑧"	U2467 # CIRCLED DIGIT EIGHT
<Multi_key> <parenleft> <KP_8> <parenright>		: "⑧"	U2467 # CIRCLED DIGIT EIGHT
<Multi_key> <parenleft> <9> <parenright>		: "⑨"	U2468 # CIRCLED DIGIT NINE
<Multi_key> <parenleft> <KP_9> <parenright>		: "⑨"	U2468 # CIRCLED DIGIT NINE
<Multi_key> <parenleft> <1> <0> <parenright>		: "⑩"	U2469 # CIRCLED NUMBER TEN
<Multi_key> <parenleft> <KP_1> <KP_0> <parenright>	: "⑩"	U2469 # CIRCLED NUMBER TEN
<Multi_key> <parenleft> <1> <1> <parenright>		: "⑪"	U246A # CIRCLED NUMBER ELEVEN
<Multi_key> <parenleft> <KP_1> <KP_1> <parenright>	: "⑪"	U246A # CIRCLED NUMBER ELEVEN
<Multi_key> <parenleft> <1> <2> <parenright>		: "⑫"	U246B # CIRCLED NUMBER TWELVE
<Multi_key> <parenleft> <KP_1> <KP_2> <parenright>	: "⑫"	U246B # CIRCLED NUMBER TWELVE
<Multi_key> <parenleft> <1> <3> <parenright>		: "⑬"	U246C # CIRCLED NUMBER THIRTEEN
<Multi_key> <parenleft> <KP_1> <KP_3> <parenright>	: "⑬"	U246C # CIRCLED NUMBER THIRTEEN
<Multi_key> <parenleft> <1> <4> <parenright>		: "⑭"	U246D # CIRCLED NUMBER FOURTEEN
<Multi_key> <parenleft> <KP_1> <KP_4> <parenright>	: "⑭"	U246D # CIRCLED NUMBER FOURTEEN
<Multi_key> <parenleft> <1> <5> <parenright>		: "⑮"	U246E # CIRCLED NUMBER FIFTEEN
<Multi_key> <parenleft> <KP_1> <KP_5> <parenright>	: "⑮"	U246E # CIRCLED NUMBER FIFTEEN
<Multi_key> <parenleft> <1> <6> <parenright>		: "⑯"	U246F # CIRCLED NUMBER SIXTEEN
<Multi_key> <parenleft> <KP_1> <KP_6> <parenright>	: "⑯"	U246F # CIRCLED NUMBER SIXTEEN
<Multi_key> <parenleft> <1> <7> <parenright>		: "⑰"	U2470 # CIRCLED NUMBER SEVENTEEN
<Multi_key> <parenleft> <KP_1> <KP_7> <parenright>	: "⑰"	U2470 # CIRCLED NUMBER SEVENTEEN
<Multi_key> <parenleft> <1> <8> <parenright>		: "⑱"	U2471 # CIRCLED NUMBER EIGHTEEN
<Multi_key> <parenleft> <KP_1> <KP_8> <parenright>	: "⑱"	U2471 # CIRCLED NUMBER EIGHTEEN
<Multi_key> <parenleft> <1> <9> <parenright>		: "⑲"	U2472 # CIRCLED NUMBER NINETEEN
<Multi_key> <parenleft> <KP_1> <KP_9> <parenright>	: "⑲"	U2472 # CIRCLED NUMBER NINETEEN
<Multi_key> <parenleft> <2> <0> <parenright>		: "⑳"	U2473 # CIRCLED NUMBER TWENTY
<Multi_key> <parenleft> <KP_2> <KP_0> <parenright>	: "⑳"	U2473 # CIRCLED NUMBER TWENTY
<Multi_key> <parenleft> <A> <parenright>	: "Ⓐ"	U24B6 # CIRCLED LATIN CAPITAL LETTER A
<Multi_key> <parenleft> <B> <parenright>	: "Ⓑ"	U24B7 # CIRCLED LATIN CAPITAL LETTER B
<Multi_key> <parenleft> <C> <parenright>	: "Ⓒ"	U24B8 # CIRCLED LATIN CAPITAL LETTER C
<Multi_key> <parenleft> <D> <parenright>	: "Ⓓ"	U24B9 # CIRCLED LATIN CAPITAL LETTER D
<Multi_key> <parenleft> <E> <parenright>	: "Ⓔ"	U24BA # CIRCLED LATIN CAPITAL LETTER E
<Multi_key> <parenleft> <F> <parenright>	: "Ⓕ"	U24BB # CIRCLED LATIN CAPITAL LETTER F
<Multi_key> <parenleft> <G> <parenright>	: "Ⓖ"	U24BC # CIRCLED LATIN CAPITAL LETTER G
<Multi_key> <parenleft> <H> <parenright>	: "Ⓗ"	U24BD # CIRCLED LATIN CAPITAL LETTER H
<Multi_key> <parenleft> <I> <parenright>	: "Ⓘ"	U24BE # CIRCLED LATIN CAPITAL LETTER I
<Multi_key> <parenleft> <J> <parenright>	: "Ⓙ"	U24BF # CIRCLED LATIN CAPITAL LETTER J
<Multi_key> <parenleft> <K> <parenright>	: "Ⓚ"	U24C0 # CIRCLED LATIN CAPITAL LETTER K
<Multi_key> <parenleft> <L> <parenright>	: "Ⓛ"	U24C1 # CIRCLED LATIN CAPITAL LETTER L
<Multi_key> <parenleft> <M> <parenright>	: "Ⓜ"	U24C2 # CIRCLED LATIN CAPITAL LETTER M
<Multi_key> <parenleft> <N> <parenright>	: "Ⓝ"	U24C3 # CIRCLED LATIN CAPITAL LETTER N
<Multi_key> <parenleft> <O> <parenright>	: "Ⓞ"	U24C4 # CIRCLED LATIN CAPITAL LETTER O
<Multi_key> <parenleft> <P> <parenright>	: "Ⓟ"	U24C5 # CIRCLED LATIN CAPITAL LETTER P
<Multi_key> <parenleft> <Q> <parenright>	: "Ⓠ"	U24C6 # CIRCLED LATIN CAPITAL LETTER Q
<Multi_key> <parenleft> <R> <parenright>	: "Ⓡ"	U24C7 # CIRCLED LATIN CAPITAL LETTER R
<Multi_key> <parenleft> <S> <parenright>	: "Ⓢ"	U24C8 # CIRCLED LATIN CAPITAL LETTER S
<Multi_key> <parenleft> <T> <parenright>	: "Ⓣ"	U24C9 # CIRCLED LATIN CAPITAL LETTER T
<Multi_key> <parenleft> <U> <parenright>	: "Ⓤ"	U24CA # CIRCLED LATIN CAPITAL LETTER U
<Multi_key> <parenleft> <V> <parenright>	: "Ⓥ"	U24CB # CIRCLED LATIN CAPITAL LETTER V
<Multi_key> <parenleft> <W> <parenright>	: "Ⓦ"	U24CC # CIRCLED LATIN CAPITAL LETTER W
<Multi_key> <parenleft> <X> <parenright>	: "Ⓧ"	U24CD # CIRCLED LATIN CAPITAL LETTER X
<Multi_key> <parenleft> <Y> <parenright>	: "Ⓨ"	U24CE # CIRCLED LATIN CAPITAL LETTER Y
<Multi_key> <parenleft> <Z> <parenright>	: "Ⓩ"	U24CF # CIRCLED LATIN CAPITAL LETTER Z
<Multi_key> <parenleft> <a> <parenright>	: "ⓐ"	U24D0 # CIRCLED LATIN SMALL LETTER A
<Multi_key> <parenleft> <b> <parenright>	: "ⓑ"	U24D1 # CIRCLED LATIN SMALL LETTER B
<Multi_key> <parenleft> <c> <parenright>	: "ⓒ"	U24D2 # CIRCLED LATIN SMALL LETTER C
<Multi_key> <parenleft> <d> <parenright>	: "ⓓ"	U24D3 # CIRCLED LATIN SMALL LETTER D
<Multi_key> <parenleft> <e> <parenright>	: "ⓔ"	U24D4 # CIRCLED LATIN SMALL LETTER E
<Multi_key> <parenleft> <f> <parenright>	: "ⓕ"	U24D5 # CIRCLED LATIN SMALL LETTER F
<Multi_key> <parenleft> <g> <parenright>	: "ⓖ"	U24D6 # CIRCLED LATIN SMALL LETTER G
<Multi_key> <parenleft> <h> <parenright>	: "ⓗ"	U24D7 # CIRCLED LATIN SMALL LETTER H
<Multi_key> <parenleft> <i> <parenright>	: "ⓘ"	U24D8 # CIRCLED LATIN SMALL LETTER I
<Multi_key> <parenleft> <j> <parenright>	: "ⓙ"	U24D9 # CIRCLED LATIN SMALL LETTER J
<Multi_key> <parenleft> <k> <parenright>	: "ⓚ"	U24DA # CIRCLED LATIN SMALL LETTER K
<Multi_key> <parenleft> <l> <parenright>	: "ⓛ"	U24DB # CIRCLED LATIN SMALL LETTER L
<Multi_key> <parenleft> <m> <parenright>	: "ⓜ"	U24DC # CIRCLED LATIN SMALL LETTER M
<Multi_key> <parenleft> <n> <parenright>	: "ⓝ"	U24DD # CIRCLED LATIN SMALL LETTER N
<Multi_key> <parenleft> <o> <parenright>	: "ⓞ"	U24DE # CIRCLED LATIN SMALL LETTER O
<Multi_key> <parenleft> <p> <parenright>	: "ⓟ"	U24DF # CIRCLED LATIN SMALL LETTER P
<Multi_key> <parenleft> <q> <parenright>	: "ⓠ"	U24E0 # CIRCLED LATIN SMALL LETTER Q
<Multi_key> <parenleft> <r> <parenright>	: "ⓡ"	U24E1 # CIRCLED LATIN SMALL LETTER R
<Multi_key> <parenleft> <s> <parenright>	: "ⓢ"	U24E2 # CIRCLED LATIN SMALL LETTER S
<Multi_key> <parenleft> <t> <parenright>	: "ⓣ"	U24E3 # CIRCLED LATIN SMALL LETTER T
<Multi_key> <parenleft> <u> <parenright>	: "ⓤ"	U24E4 # CIRCLED LATIN SMALL LETTER U
<Multi_key> <parenleft> <v> <parenright>	: "ⓥ"	U24E5 # CIRCLED LATIN SMALL LETTER V
<Multi_key> <parenleft> <w> <parenright>	: "ⓦ"	U24E6 # CIRCLED LATIN SMALL LETTER W
<Multi_key> <parenleft> <x> <parenright>	: "ⓧ"	U24E7 # CIRCLED LATIN SMALL LETTER X
<Multi_key> <parenleft> <y> <parenright>	: "ⓨ"	U24E8 # CIRCLED LATIN SMALL LETTER Y
<Multi_key> <parenleft> <z> <parenright>	: "ⓩ"	U24E9 # CIRCLED LATIN SMALL LETTER Z
<Multi_key> <parenleft> <0> <parenright>	: "⓪"	U24EA # CIRCLED DIGIT ZERO
<Multi_key> <parenleft> <KP_0> <parenright>	: "⓪"	U24EA # CIRCLED DIGIT ZERO
# Supplemental Mathematical Operators
<dead_belowdot> <plus>				: "⨥"	U2A25 # PLUS SIGN WITH DOT BELOW
<dead_belowtilde> <plus>			: "⨦"	U2A26 # PLUS SIGN WITH TILDE BELOW
<dead_belowdot> <minus>				: "⨪"	U2A2A # MINUS SIGN WITH DOT BELOW
<dead_belowdot> <equal>				: "⩦"	U2A66 # EQUALS SIGN WITH DOT BELOW
<dead_diaeresis> <dead_belowdiaeresis> <equal>	: "⩷"	U2A77 # EQUALS SIGN WITH TWO DOTS ABOVE AND TWO DOTS BELOW
<dead_belowdiaeresis> <dead_diaeresis> <equal>	: "⩷"	U2A77 # EQUALS SIGN WITH TWO DOTS ABOVE AND TWO DOTS BELOW
<Multi_key> <U2ADD> <slash>			: "⫝̸"	U2ADC # FORKING
<dead_belowring> <bar>				: "⫰"	U2AF0 # VERTICAL LINE WITH CIRCLE BELOW
# Hiragana
<dead_voiced_sound> <U304B>		: "が"	U304C # HIRAGANA LETTER GA
<dead_voiced_sound> <U304D>		: "ぎ"	U304E # HIRAGANA LETTER GI
<dead_voiced_sound> <U304F>		: "ぐ"	U3050 # HIRAGANA LETTER GU
<dead_voiced_sound> <U3051>		: "げ"	U3052 # HIRAGANA LETTER GE
<dead_voiced_sound> <U3053>		: "ご"	U3054 # HIRAGANA LETTER GO
<dead_voiced_sound> <U3055>		: "ざ"	U3056 # HIRAGANA LETTER ZA
<dead_voiced_sound> <U3057>		: "じ"	U3058 # HIRAGANA LETTER ZI
<dead_voiced_sound> <U3059>		: "ず"	U305A # HIRAGANA LETTER ZU
<dead_voiced_sound> <U305B>		: "ぜ"	U305C # HIRAGANA LETTER ZE
<dead_voiced_sound> <U305D>		: "ぞ"	U305E # HIRAGANA LETTER ZO
<dead_voiced_sound> <U305F>		: "だ"	U3060 # HIRAGANA LETTER DA
<dead_voiced_sound> <U3061>		: "ぢ"	U3062 # HIRAGANA LETTER DI
<dead_voiced_sound> <U3064>		: "づ"	U3065 # HIRAGANA LETTER DU
<dead_voiced_sound> <U3066>		: "で"	U3067 # HIRAGANA LETTER DE
<dead_voiced_sound> <U3068>		: "ど"	U3069 # HIRAGANA LETTER DO
<dead_voiced_sound> <U306F>		: "ば"	U3070 # HIRAGANA LETTER BA
<dead_semivoiced_sound> <U306F>		: "ぱ"	U3071 # HIRAGANA LETTER PA
<dead_voiced_sound> <U3072>		: "び"	U3073 # HIRAGANA LETTER BI
<dead_semivoiced_sound> <U3072>		: "ぴ"	U3074 # HIRAGANA LETTER PI
<dead_voiced_sound> <U3075>		: "ぶ"	U3076 # HIRAGANA LETTER BU
<dead_semivoiced_sound> <U3075>		: "ぷ"	U3077 # HIRAGANA LETTER PU
<dead_voiced_sound> <U3078>		: "べ"	U3079 # HIRAGANA LETTER BE
<dead_semivoiced_sound> <U3078>		: "ぺ"	U307A # HIRAGANA LETTER PE
<dead_voiced_sound> <U307B>		: "ぼ"	U307C # HIRAGANA LETTER BO
<dead_semivoiced_sound> <U307B>		: "ぽ"	U307D # HIRAGANA LETTER PO
<dead_voiced_sound> <U3046>		: "ゔ"	U3094 # HIRAGANA LETTER VU
<dead_voiced_sound> <U309D>		: "ゞ"	U309E # HIRAGANA VOICED ITERATION MARK
# Katakana
<dead_voiced_sound> <kana_KA>		: "ガ"	U30AC # KATAKANA LETTER GA
<dead_voiced_sound> <kana_KI>		: "ギ"	U30AE # KATAKANA LETTER GI
<dead_voiced_sound> <kana_KU>		: "グ"	U30B0 # KATAKANA LETTER GU
<dead_voiced_sound> <kana_KE>		: "ゲ"	U30B2 # KATAKANA LETTER GE
<dead_voiced_sound> <kana_KO>		: "ゴ"	U30B4 # KATAKANA LETTER GO
<dead_voiced_sound> <kana_SA>		: "ザ"	U30B6 # KATAKANA LETTER ZA
<dead_voiced_sound> <kana_SHI>		: "ジ"	U30B8 # KATAKANA LETTER ZI
<dead_voiced_sound> <kana_SU>		: "ズ"	U30BA # KATAKANA LETTER ZU
<dead_voiced_sound> <kana_SE>		: "ゼ"	U30BC # KATAKANA LETTER ZE
<dead_voiced_sound> <kana_SO>		: "ゾ"	U30BE # KATAKANA LETTER ZO
<dead_voiced_sound> <kana_TA>		: "ダ"	U30C0 # KATAKANA LETTER DA
<dead_voiced_sound> <kana_CHI>		: "ヂ"	U30C2 # KATAKANA LETTER DI
<dead_voiced_sound> <kana_TSU>		: "ヅ"	U30C5 # KATAKANA LETTER DU
<dead_voiced_sound> <kana_TE>		: "デ"	U30C7 # KATAKANA LETTER DE
<dead_voiced_sound> <kana_TO>		: "ド"	U30C9 # KATAKANA LETTER DO
<dead_voiced_sound> <kana_HA>		: "バ"	U30D0 # KATAKANA LETTER BA
<dead_semivoiced_sound> <kana_HA>	: "パ"	U30D1 # KATAKANA LETTER PA
<dead_voiced_sound> <kana_HI>		: "ビ"	U30D3 # KATAKANA LETTER BI
<dead_semivoiced_sound> <kana_HI>	: "ピ"	U30D4 # KATAKANA LETTER PI
<dead_voiced_sound> <kana_FU>		: "ブ"	U30D6 # KATAKANA LETTER BU
<dead_semivoiced_sound> <kana_FU>	: "プ"	U30D7 # KATAKANA LETTER PU
<dead_voiced_sound> <kana_HE>		: "ベ"	U30D9 # KATAKANA LETTER BE
<dead_semivoiced_sound> <kana_HE>	: "ペ"	U30DA # KATAKANA LETTER PE
<dead_voiced_sound> <kana_HO>		: "ボ"	U30DC # KATAKANA LETTER BO
<dead_semivoiced_sound> <kana_HO>	: "ポ"	U30DD # KATAKANA LETTER PO
<dead_voiced_sound> <kana_U>		: "ヴ"	U30F4 # KATAKANA LETTER VU
<dead_voiced_sound> <kana_WA>		: "ヷ"	U30F7 # KATAKANA LETTER VA
<dead_voiced_sound> <U30F0>		: "ヸ"	U30F8 # KATAKANA LETTER VI
<dead_voiced_sound> <U30F1>		: "ヹ"	U30F9 # KATAKANA LETTER VE
<dead_voiced_sound> <kana_WO>		: "ヺ"	U30FA # KATAKANA LETTER VO
<dead_voiced_sound> <U30FD>		: "ヾ"	U30FE # KATAKANA VOICED ITERATION MARK
# Kanbun
<dead_circumflex> <U4E00>		: "㆒"	U3192 # IDEOGRAPHIC ANNOTATION ONE MARK
<Multi_key> <asciicircum> <U4E00>	: "㆒"	U3192 # IDEOGRAPHIC ANNOTATION ONE MARK
<dead_circumflex> <U4E8C>		: "㆓"	U3193 # IDEOGRAPHIC ANNOTATION TWO MARK
<Multi_key> <asciicircum> <U4E8C>	: "㆓"	U3193 # IDEOGRAPHIC ANNOTATION TWO MARK
<dead_circumflex> <U4E09>		: "㆔"	U3194 # IDEOGRAPHIC ANNOTATION THREE MARK
<Multi_key> <asciicircum> <U4E09>	: "㆔"	U3194 # IDEOGRAPHIC ANNOTATION THREE MARK
<dead_circumflex> <U56DB>		: "㆕"	U3195 # IDEOGRAPHIC ANNOTATION FOUR MARK
<Multi_key> <asciicircum> <U56DB>	: "㆕"	U3195 # IDEOGRAPHIC ANNOTATION FOUR MARK
<dead_circumflex> <U4E0A>		: "㆖"	U3196 # IDEOGRAPHIC ANNOTATION TOP MARK
<Multi_key> <asciicircum> <U4E0A>	: "㆖"	U3196 # IDEOGRAPHIC ANNOTATION TOP MARK
<dead_circumflex> <U4E2D>		: "㆗"	U3197 # IDEOGRAPHIC ANNOTATION MIDDLE MARK
<Multi_key> <asciicircum> <U4E2D>	: "㆗"	U3197 # IDEOGRAPHIC ANNOTATION MIDDLE MARK
<dead_circumflex> <U4E0B>		: "㆘"	U3198 # IDEOGRAPHIC ANNOTATION BOTTOM MARK
<Multi_key> <asciicircum> <U4E0B>	: "㆘"	U3198 # IDEOGRAPHIC ANNOTATION BOTTOM MARK
<dead_circumflex> <U7532>		: "㆙"	U3199 # IDEOGRAPHIC ANNOTATION FIRST MARK
<Multi_key> <asciicircum> <U7532>	: "㆙"	U3199 # IDEOGRAPHIC ANNOTATION FIRST MARK
<dead_circumflex> <U4E59>		: "㆚"	U319A # IDEOGRAPHIC ANNOTATION SECOND MARK
<Multi_key> <asciicircum> <U4E59>	: "㆚"	U319A # IDEOGRAPHIC ANNOTATION SECOND MARK
<dead_circumflex> <U4E19>		: "㆛"	U319B # IDEOGRAPHIC ANNOTATION THIRD MARK
<Multi_key> <asciicircum> <U4E19>	: "㆛"	U319B # IDEOGRAPHIC ANNOTATION THIRD MARK
<dead_circumflex> <U4E01>		: "㆜"	U319C # IDEOGRAPHIC ANNOTATION FOURTH MARK
<Multi_key> <asciicircum> <U4E01>	: "㆜"	U319C # IDEOGRAPHIC ANNOTATION FOURTH MARK
<dead_circumflex> <U5929>		: "㆝"	U319D # IDEOGRAPHIC ANNOTATION HEAVEN MARK
<Multi_key> <asciicircum> <U5929>	: "㆝"	U319D # IDEOGRAPHIC ANNOTATION HEAVEN MARK
<dead_circumflex> <U5730>		: "㆞"	U319E # IDEOGRAPHIC ANNOTATION EARTH MARK
<Multi_key> <asciicircum> <U5730>	: "㆞"	U319E # IDEOGRAPHIC ANNOTATION EARTH MARK
<dead_circumflex> <U4EBA>		: "㆟"	U319F # IDEOGRAPHIC ANNOTATION MAN MARK
<Multi_key> <asciicircum> <U4EBA>	: "㆟"	U319F # IDEOGRAPHIC ANNOTATION MAN MARK
# Enclosed CJK Letters and Months
<Multi_key> <parenleft> <2> <1> <parenright>		: "㉑"	U3251 # CIRCLED NUMBER TWENTY ONE
<Multi_key> <parenleft> <KP_2> <KP_1> <parenright>	: "㉑"	U3251 # CIRCLED NUMBER TWENTY ONE
<Multi_key> <parenleft> <2> <2> <parenright>		: "㉒"	U3252 # CIRCLED NUMBER TWENTY TWO
<Multi_key> <parenleft> <KP_2> <KP_2> <parenright>	: "㉒"	U3252 # CIRCLED NUMBER TWENTY TWO
<Multi_key> <parenleft> <2> <3> <parenright>		: "㉓"	U3253 # CIRCLED NUMBER TWENTY THREE
<Multi_key> <parenleft> <KP_2> <KP_3> <parenright>	: "㉓"	U3253 # CIRCLED NUMBER TWENTY THREE
<Multi_key> <parenleft> <2> <4> <parenright>		: "㉔"	U3254 # CIRCLED NUMBER TWENTY FOUR
<Multi_key> <parenleft> <KP_2> <KP_4> <parenright>	: "㉔"	U3254 # CIRCLED NUMBER TWENTY FOUR
<Multi_key> <parenleft> <2> <5> <parenright>		: "㉕"	U3255 # CIRCLED NUMBER TWENTY FIVE
<Multi_key> <parenleft> <KP_2> <KP_5> <parenright>	: "㉕"	U3255 # CIRCLED NUMBER TWENTY FIVE
<Multi_key> <parenleft> <2> <6> <parenright>		: "㉖"	U3256 # CIRCLED NUMBER TWENTY SIX
<Multi_key> <parenleft> <KP_2> <KP_6> <parenright>	: "㉖"	U3256 # CIRCLED NUMBER TWENTY SIX
<Multi_key> <parenleft> <2> <7> <parenright>		: "㉗"	U3257 # CIRCLED NUMBER TWENTY SEVEN
<Multi_key> <parenleft> <KP_2> <KP_7> <parenright>	: "㉗"	U3257 # CIRCLED NUMBER TWENTY SEVEN
<Multi_key> <parenleft> <2> <8> <parenright>		: "㉘"	U3258 # CIRCLED NUMBER TWENTY EIGHT
<Multi_key> <parenleft> <KP_2> <KP_8> <parenright>	: "㉘"	U3258 # CIRCLED NUMBER TWENTY EIGHT
<Multi_key> <parenleft> <2> <9> <parenright>		: "㉙"	U3259 # CIRCLED NUMBER TWENTY NINE
<Multi_key> <parenleft> <KP_2> <KP_9> <parenright>	: "㉙"	U3259 # CIRCLED NUMBER TWENTY NINE
<Multi_key> <parenleft> <3> <0> <parenright>		: "㉚"	U325A # CIRCLED NUMBER THIRTY
<Multi_key> <parenleft> <KP_3> <KP_0> <parenright>	: "㉚"	U325A # CIRCLED NUMBER THIRTY
<Multi_key> <parenleft> <3> <1> <parenright>		: "㉛"	U325B # CIRCLED NUMBER THIRTY ONE
<Multi_key> <parenleft> <KP_3> <KP_1> <parenright>	: "㉛"	U325B # CIRCLED NUMBER THIRTY ONE
<Multi_key> <parenleft> <3> <2> <parenright>		: "㉜"	U325C # CIRCLED NUMBER THIRTY TWO
<Multi_key> <parenleft> <KP_3> <KP_2> <parenright>	: "㉜"	U325C # CIRCLED NUMBER THIRTY TWO
<Multi_key> <parenleft> <3> <3> <parenright>		: "㉝"	U325D # CIRCLED NUMBER THIRTY THREE
<Multi_key> <parenleft> <KP_3> <KP_3> <parenright>	: "㉝"	U325D # CIRCLED NUMBER THIRTY THREE
<Multi_key> <parenleft> <3> <4> <parenright>		: "㉞"	U325E # CIRCLED NUMBER THIRTY FOUR
<Multi_key> <parenleft> <KP_3> <KP_4> <parenright>	: "㉞"	U325E # CIRCLED NUMBER THIRTY FOUR
<Multi_key> <parenleft> <3> <5> <parenright>		: "㉟"	U325F # CIRCLED NUMBER THIRTY FIVE
<Multi_key> <parenleft> <KP_3> <KP_5> <parenright>	: "㉟"	U325F # CIRCLED NUMBER THIRTY FIVE
<Multi_key> <parenleft> <U1100> <parenright>		: "㉠"	U3260 # CIRCLED HANGUL KIYEOK
<Multi_key> <parenleft> <U1102> <parenright>		: "㉡"	U3261 # CIRCLED HANGUL NIEUN
<Multi_key> <parenleft> <U1103> <parenright>		: "㉢"	U3262 # CIRCLED HANGUL TIKEUT
<Multi_key> <parenleft> <U1105> <parenright>		: "㉣"	U3263 # CIRCLED HANGUL RIEUL
<Multi_key> <parenleft> <U1106> <parenright>		: "㉤"	U3264 # CIRCLED HANGUL MIEUM
<Multi_key> <parenleft> <U1107> <parenright>		: "㉥"	U3265 # CIRCLED HANGUL PIEUP
<Multi_key> <parenleft> <U1109> <parenright>		: "㉦"	U3266 # CIRCLED HANGUL SIOS
<Multi_key> <parenleft> <U110B> <parenright>		: "㉧"	U3267 # CIRCLED HANGUL IEUNG
<Multi_key> <parenleft> <U110C> <parenright>		: "㉨"	U3268 # CIRCLED HANGUL CIEUC
<Multi_key> <parenleft> <U110E> <parenright>		: "㉩"	U3269 # CIRCLED HANGUL CHIEUCH
<Multi_key> <parenleft> <U110F> <parenright>		: "㉪"	U326A # CIRCLED HANGUL KHIEUKH
<Multi_key> <parenleft> <U1110> <parenright>		: "㉫"	U326B # CIRCLED HANGUL THIEUTH
<Multi_key> <parenleft> <U1111> <parenright>		: "㉬"	U326C # CIRCLED HANGUL PHIEUPH
<Multi_key> <parenleft> <U1112> <parenright>		: "㉭"	U326D # CIRCLED HANGUL HIEUH
<Multi_key> <parenleft> <U1100> <U1161> <parenright>	: "㉮"	U326E # CIRCLED HANGUL KIYEOK A
<Multi_key> <parenleft> <U1102> <U1161> <parenright>	: "㉯"	U326F # CIRCLED HANGUL NIEUN A
<Multi_key> <parenleft> <U1103> <U1161> <parenright>	: "㉰"	U3270 # CIRCLED HANGUL TIKEUT A
<Multi_key> <parenleft> <U1105> <U1161> <parenright>	: "㉱"	U3271 # CIRCLED HANGUL RIEUL A
<Multi_key> <parenleft> <U1106> <U1161> <parenright>	: "㉲"	U3272 # CIRCLED HANGUL MIEUM A
<Multi_key> <parenleft> <U1107> <U1161> <parenright>	: "㉳"	U3273 # CIRCLED HANGUL PIEUP A
<Multi_key> <parenleft> <U1109> <U1161> <parenright>	: "㉴"	U3274 # CIRCLED HANGUL SIOS A
<Multi_key> <parenleft> <U110B> <U1161> <parenright>	: "㉵"	U3275 # CIRCLED HANGUL IEUNG A
<Multi_key> <parenleft> <U110C> <U1161> <parenright>	: "㉶"	U3276 # CIRCLED HANGUL CIEUC A
<Multi_key> <parenleft> <U110E> <U1161> <parenright>	: "㉷"	U3277 # CIRCLED HANGUL CHIEUCH A
<Multi_key> <parenleft> <U110F> <U1161> <parenright>	: "㉸"	U3278 # CIRCLED HANGUL KHIEUKH A
<Multi_key> <parenleft> <U1110> <U1161> <parenright>	: "㉹"	U3279 # CIRCLED HANGUL THIEUTH A
<Multi_key> <parenleft> <U1111> <U1161> <parenright>	: "㉺"	U327A # CIRCLED HANGUL PHIEUPH A
<Multi_key> <parenleft> <U1112> <U1161> <parenright>	: "㉻"	U327B # CIRCLED HANGUL HIEUH A
<Multi_key> <parenleft> <U4E00> <parenright>	: "㊀"	U3280 # CIRCLED IDEOGRAPH ONE
<Multi_key> <parenleft> <U4E8C> <parenright>	: "㊁"	U3281 # CIRCLED IDEOGRAPH TWO
<Multi_key> <parenleft> <U4E09> <parenright>	: "㊂"	U3282 # CIRCLED IDEOGRAPH THREE
<Multi_key> <parenleft> <U56DB> <parenright>	: "㊃"	U3283 # CIRCLED IDEOGRAPH FOUR
<Multi_key> <parenleft> <U4E94> <parenright>	: "㊄"	U3284 # CIRCLED IDEOGRAPH FIVE
<Multi_key> <parenleft> <U516D> <parenright>	: "㊅"	U3285 # CIRCLED IDEOGRAPH SIX
<Multi_key> <parenleft> <U4E03> <parenright>	: "㊆"	U3286 # CIRCLED IDEOGRAPH SEVEN
<Multi_key> <parenleft> <U516B> <parenright>	: "㊇"	U3287 # CIRCLED IDEOGRAPH EIGHT
<Multi_key> <parenleft> <U4E5D> <parenright>	: "㊈"	U3288 # CIRCLED IDEOGRAPH NINE
<Multi_key> <parenleft> <U5341> <parenright>	: "㊉"	U3289 # CIRCLED IDEOGRAPH TEN
<Multi_key> <parenleft> <U6708> <parenright>	: "㊊"	U328A # CIRCLED IDEOGRAPH MOON
<Multi_key> <parenleft> <U706B> <parenright>	: "㊋"	U328B # CIRCLED IDEOGRAPH FIRE
<Multi_key> <parenleft> <U6C34> <parenright>	: "㊌"	U328C # CIRCLED IDEOGRAPH WATER
<Multi_key> <parenleft> <U6728> <parenright>	: "㊍"	U328D # CIRCLED IDEOGRAPH WOOD
<Multi_key> <parenleft> <U91D1> <parenright>	: "㊎"	U328E # CIRCLED IDEOGRAPH METAL
<Multi_key> <parenleft> <U571F> <parenright>	: "㊏"	U328F # CIRCLED IDEOGRAPH EARTH
<Multi_key> <parenleft> <U65E5> <parenright>	: "㊐"	U3290 # CIRCLED IDEOGRAPH SUN
<Multi_key> <parenleft> <U682A> <parenright>	: "㊑"	U3291 # CIRCLED IDEOGRAPH STOCK
<Multi_key> <parenleft> <U6709> <parenright>	: "㊒"	U3292 # CIRCLED IDEOGRAPH HAVE
<Multi_key> <parenleft> <U793E> <parenright>	: "㊓"	U3293 # CIRCLED IDEOGRAPH SOCIETY
<Multi_key> <parenleft> <U540D> <parenright>	: "㊔"	U3294 # CIRCLED IDEOGRAPH NAME
<Multi_key> <parenleft> <U7279> <parenright>	: "㊕"	U3295 # CIRCLED IDEOGRAPH SPECIAL
<Multi_key> <parenleft> <U8CA1> <parenright>	: "㊖"	U3296 # CIRCLED IDEOGRAPH FINANCIAL
<Multi_key> <parenleft> <U795D> <parenright>	: "㊗"	U3297 # CIRCLED IDEOGRAPH CONGRATULATION
<Multi_key> <parenleft> <U52B4> <parenright>	: "㊘"	U3298 # CIRCLED IDEOGRAPH LABOR
<Multi_key> <parenleft> <U79D8> <parenright>	: "㊙"	U3299 # CIRCLED IDEOGRAPH SECRET
<Multi_key> <parenleft> <U7537> <parenright>	: "㊚"	U329A # CIRCLED IDEOGRAPH MALE
<Multi_key> <parenleft> <U5973> <parenright>	: "㊛"	U329B # CIRCLED IDEOGRAPH FEMALE
<Multi_key> <parenleft> <U9069> <parenright>	: "㊜"	U329C # CIRCLED IDEOGRAPH SUITABLE
<Multi_key> <parenleft> <U512A> <parenright>	: "㊝"	U329D # CIRCLED IDEOGRAPH EXCELLENT
<Multi_key> <parenleft> <U5370> <parenright>	: "㊞"	U329E # CIRCLED IDEOGRAPH PRINT
<Multi_key> <parenleft> <U6CE8> <parenright>	: "㊟"	U329F # CIRCLED IDEOGRAPH ATTENTION
<Multi_key> <parenleft> <U9805> <parenright>	: "㊠"	U32A0 # CIRCLED IDEOGRAPH ITEM
<Multi_key> <parenleft> <U4F11> <parenright>	: "㊡"	U32A1 # CIRCLED IDEOGRAPH REST
<Multi_key> <parenleft> <U5199> <parenright>	: "㊢"	U32A2 # CIRCLED IDEOGRAPH COPY
<Multi_key> <parenleft> <U6B63> <parenright>	: "㊣"	U32A3 # CIRCLED IDEOGRAPH CORRECT
<Multi_key> <parenleft> <U4E0A> <parenright>	: "㊤"	U32A4 # CIRCLED IDEOGRAPH HIGH
<Multi_key> <parenleft> <U4E2D> <parenright>	: "㊥"	U32A5 # CIRCLED IDEOGRAPH CENTRE
<Multi_key> <parenleft> <U4E0B> <parenright>	: "㊦"	U32A6 # CIRCLED IDEOGRAPH LOW
<Multi_key> <parenleft> <U5DE6> <parenright>	: "㊧"	U32A7 # CIRCLED IDEOGRAPH LEFT
<Multi_key> <parenleft> <U53F3> <parenright>	: "㊨"	U32A8 # CIRCLED IDEOGRAPH RIGHT
<Multi_key> <parenleft> <U533B> <parenright>	: "㊩"	U32A9 # CIRCLED IDEOGRAPH MEDICINE
<Multi_key> <parenleft> <U5B97> <parenright>	: "㊪"	U32AA # CIRCLED IDEOGRAPH RELIGION
<Multi_key> <parenleft> <U5B66> <parenright>	: "㊫"	U32AB # CIRCLED IDEOGRAPH STUDY
<Multi_key> <parenleft> <U76E3> <parenright>	: "㊬"	U32AC # CIRCLED IDEOGRAPH SUPERVISE
<Multi_key> <parenleft> <U4F01> <parenright>	: "㊭"	U32AD # CIRCLED IDEOGRAPH ENTERPRISE
<Multi_key> <parenleft> <U8CC7> <parenright>	: "㊮"	U32AE # CIRCLED IDEOGRAPH RESOURCE
<Multi_key> <parenleft> <U5354> <parenright>	: "㊯"	U32AF # CIRCLED IDEOGRAPH ALLIANCE
<Multi_key> <parenleft> <U591C> <parenright>	: "㊰"	U32B0 # CIRCLED IDEOGRAPH NIGHT
<Multi_key> <parenleft> <3> <6> <parenright>		: "㊱"	U32B1 # CIRCLED NUMBER THIRTY SIX
<Multi_key> <parenleft> <KP_3> <KP_6> <parenright>	: "㊱"	U32B1 # CIRCLED NUMBER THIRTY SIX
<Multi_key> <parenleft> <3> <7> <parenright>		: "㊲"	U32B2 # CIRCLED NUMBER THIRTY SEVEN
<Multi_key> <parenleft> <KP_3> <KP_7> <parenright>	: "㊲"	U32B2 # CIRCLED NUMBER THIRTY SEVEN
<Multi_key> <parenleft> <3> <8> <parenright>		: "㊳"	U32B3 # CIRCLED NUMBER THIRTY EIGHT
<Multi_key> <parenleft> <KP_3> <KP_8> <parenright>	: "㊳"	U32B3 # CIRCLED NUMBER THIRTY EIGHT
<Multi_key> <parenleft> <3> <9> <parenright>		: "㊴"	U32B4 # CIRCLED NUMBER THIRTY NINE
<Multi_key> <parenleft> <KP_3> <KP_9> <parenright>	: "㊴"	U32B4 # CIRCLED NUMBER THIRTY NINE
<Multi_key> <parenleft> <4> <0> <parenright>		: "㊵"	U32B5 # CIRCLED NUMBER FORTY
<Multi_key> <parenleft> <KP_4> <KP_0> <parenright>	: "㊵"	U32B5 # CIRCLED NUMBER FORTY
<Multi_key> <parenleft> <4> <1> <parenright>		: "㊶"	U32B6 # CIRCLED NUMBER FORTY ONE
<Multi_key> <parenleft> <KP_4> <KP_1> <parenright>	: "㊶"	U32B6 # CIRCLED NUMBER FORTY ONE
<Multi_key> <parenleft> <4> <2> <parenright>		: "㊷"	U32B7 # CIRCLED NUMBER FORTY TWO
<Multi_key> <parenleft> <KP_4> <KP_2> <parenright>	: "㊷"	U32B7 # CIRCLED NUMBER FORTY TWO
<Multi_key> <parenleft> <4> <3> <parenright>		: "㊸"	U32B8 # CIRCLED NUMBER FORTY THREE
<Multi_key> <parenleft> <KP_4> <KP_3> <parenright>	: "㊸"	U32B8 # CIRCLED NUMBER FORTY THREE
<Multi_key> <parenleft> <4> <4> <parenright>		: "㊹"	U32B9 # CIRCLED NUMBER FORTY FOUR
<Multi_key> <parenleft> <KP_4> <KP_4> <parenright>	: "㊹"	U32B9 # CIRCLED NUMBER FORTY FOUR
<Multi_key> <parenleft> <4> <5> <parenright>		: "㊺"	U32BA # CIRCLED NUMBER FORTY FIVE
<Multi_key> <parenleft> <KP_4> <KP_5> <parenright>	: "㊺"	U32BA # CIRCLED NUMBER FORTY FIVE
<Multi_key> <parenleft> <4> <6> <parenright>		: "㊻"	U32BB # CIRCLED NUMBER FORTY SIX
<Multi_key> <parenleft> <KP_4> <KP_6> <parenright>	: "㊻"	U32BB # CIRCLED NUMBER FORTY SIX
<Multi_key> <parenleft> <4> <7> <parenright>		: "㊼"	U32BC # CIRCLED NUMBER FORTY SEVEN
<Multi_key> <parenleft> <KP_4> <KP_7> <parenright>	: "㊼"	U32BC # CIRCLED NUMBER FORTY SEVEN
<Multi_key> <parenleft> <4> <8> <parenright>		: "㊽"	U32BD # CIRCLED NUMBER FORTY EIGHT
<Multi_key> <parenleft> <KP_4> <KP_8> <parenright>	: "㊽"	U32BD # CIRCLED NUMBER FORTY EIGHT
<Multi_key> <parenleft> <4> <9> <parenright>		: "㊾"	U32BE # CIRCLED NUMBER FORTY NINE
<Multi_key> <parenleft> <KP_4> <KP_9> <parenright>	: "㊾"	U32BE # CIRCLED NUMBER FORTY NINE
<Multi_key> <parenleft> <5> <0> <parenright>		: "㊿"	U32BF # CIRCLED NUMBER FIFTY
<Multi_key> <parenleft> <KP_5> <KP_0> <parenright>	: "㊿"	U32BF # CIRCLED NUMBER FIFTY
<Multi_key> <parenleft> <kana_A> <parenright>	: "㋐"	U32D0 # CIRCLED KATAKANA A
<Multi_key> <parenleft> <kana_I> <parenright>	: "㋑"	U32D1 # CIRCLED KATAKANA I
<Multi_key> <parenleft> <kana_U> <parenright>	: "㋒"	U32D2 # CIRCLED KATAKANA U
<Multi_key> <parenleft> <kana_E> <parenright>	: "㋓"	U32D3 # CIRCLED KATAKANA E
<Multi_key> <parenleft> <kana_O> <parenright>	: "㋔"	U32D4 # CIRCLED KATAKANA O
<Multi_key> <parenleft> <kana_KA> <parenright>	: "㋕"	U32D5 # CIRCLED KATAKANA KA
<Multi_key> <parenleft> <kana_KI> <parenright>	: "㋖"	U32D6 # CIRCLED KATAKANA KI
<Multi_key> <parenleft> <kana_KU> <parenright>	: "㋗"	U32D7 # CIRCLED KATAKANA KU
<Multi_key> <parenleft> <kana_KE> <parenright>	: "㋘"	U32D8 # CIRCLED KATAKANA KE
<Multi_key> <parenleft> <kana_KO> <parenright>	: "㋙"	U32D9 # CIRCLED KATAKANA KO
<Multi_key> <parenleft> <kana_SA> <parenright>	: "㋚"	U32DA # CIRCLED KATAKANA SA
<Multi_key> <parenleft> <kana_SHI> <parenright>	: "㋛"	U32DB # CIRCLED KATAKANA SI
<Multi_key> <parenleft> <kana_SU> <parenright>	: "㋜"	U32DC # CIRCLED KATAKANA SU
<Multi_key> <parenleft> <kana_SE> <parenright>	: "㋝"	U32DD # CIRCLED KATAKANA SE
<Multi_key> <parenleft> <kana_SO> <parenright>	: "㋞"	U32DE # CIRCLED KATAKANA SO
<Multi_key> <parenleft> <kana_TA> <parenright>	: "㋟"	U32DF # CIRCLED KATAKANA TA
<Multi_key> <parenleft> <kana_CHI> <parenright>	: "㋠"	U32E0 # CIRCLED KATAKANA TI
<Multi_key> <parenleft> <kana_TSU> <parenright>	: "㋡"	U32E1 # CIRCLED KATAKANA TU
<Multi_key> <parenleft> <kana_TE> <parenright>	: "㋢"	U32E2 # CIRCLED KATAKANA TE
<Multi_key> <parenleft> <kana_TO> <parenright>	: "㋣"	U32E3 # CIRCLED KATAKANA TO
<Multi_key> <parenleft> <kana_NA> <parenright>	: "㋤"	U32E4 # CIRCLED KATAKANA NA
<Multi_key> <parenleft> <kana_NI> <parenright>	: "㋥"	U32E5 # CIRCLED KATAKANA NI
<Multi_key> <parenleft> <kana_NU> <parenright>	: "㋦"	U32E6 # CIRCLED KATAKANA NU
<Multi_key> <parenleft> <kana_NE> <parenright>	: "㋧"	U32E7 # CIRCLED KATAKANA NE
<Multi_key> <parenleft> <kana_NO> <parenright>	: "㋨"	U32E8 # CIRCLED KATAKANA NO
<Multi_key> <parenleft> <kana_HA> <parenright>	: "㋩"	U32E9 # CIRCLED KATAKANA HA
<Multi_key> <parenleft> <kana_HI> <parenright>	: "㋪"	U32EA # CIRCLED KATAKANA HI
<Multi_key> <parenleft> <kana_FU> <parenright>	: "㋫"	U32EB # CIRCLED KATAKANA HU
<Multi_key> <parenleft> <kana_HE> <parenright>	: "㋬"	U32EC # CIRCLED KATAKANA HE
<Multi_key> <parenleft> <kana_HO> <parenright>	: "㋭"	U32ED # CIRCLED KATAKANA HO
<Multi_key> <parenleft> <kana_MA> <parenright>	: "㋮"	U32EE # CIRCLED KATAKANA MA
<Multi_key> <parenleft> <kana_MI> <parenright>	: "㋯"	U32EF # CIRCLED KATAKANA MI
<Multi_key> <parenleft> <kana_MU> <parenright>	: "㋰"	U32F0 # CIRCLED KATAKANA MU
<Multi_key> <parenleft> <kana_ME> <parenright>	: "㋱"	U32F1 # CIRCLED KATAKANA ME
<Multi_key> <parenleft> <kana_MO> <parenright>	: "㋲"	U32F2 # CIRCLED KATAKANA MO
<Multi_key> <parenleft> <kana_YA> <parenright>	: "㋳"	U32F3 # CIRCLED KATAKANA YA
<Multi_key> <parenleft> <kana_YU> <parenright>	: "㋴"	U32F4 # CIRCLED KATAKANA YU
<Multi_key> <parenleft> <kana_YO> <parenright>	: "㋵"	U32F5 # CIRCLED KATAKANA YO
<Multi_key> <parenleft> <kana_RA> <parenright>	: "㋶"	U32F6 # CIRCLED KATAKANA RA
<Multi_key> <parenleft> <kana_RI> <parenright>	: "㋷"	U32F7 # CIRCLED KATAKANA RI
<Multi_key> <parenleft> <kana_RU> <parenright>	: "㋸"	U32F8 # CIRCLED KATAKANA RU
<Multi_key> <parenleft> <kana_RE> <parenright>	: "㋹"	U32F9 # CIRCLED KATAKANA RE
<Multi_key> <parenleft> <kana_RO> <parenright>	: "㋺"	U32FA # CIRCLED KATAKANA RO
<Multi_key> <parenleft> <kana_WA> <parenright>	: "㋻"	U32FB # CIRCLED KATAKANA WA
<Multi_key> <parenleft> <U30F0> <parenright>	: "㋼"	U32FC # CIRCLED KATAKANA WI
<Multi_key> <parenleft> <U30F1> <parenright>	: "㋽"	U32FD # CIRCLED KATAKANA WE
<Multi_key> <parenleft> <kana_WO> <parenright>	: "㋾"	U32FE # CIRCLED KATAKANA WO
# Hebrew letters with accents
<Multi_key> <U05B4> <hebrew_yod>	: "יִ"	UFB1D # HEBREW LETTER YOD WITH HIRIQ
<Multi_key> <U05B7> <U05F2>		: "ײַ"	UFB1F # HEBREW LIGATURE YIDDISH YOD YOD PATAH
<Multi_key> <U05C1> <hebrew_shin>	: "שׁ"	UFB2A # HEBREW LETTER SHIN WITH SHIN DOT
<Multi_key> <U05C2> <hebrew_shin>	: "שׂ"	UFB2B # HEBREW LETTER SHIN WITH SIN DOT
<Multi_key> <U05C1> <UFB49>		: "שּׁ"	UFB2C # HEBREW LETTER SHIN WITH DAGESH AND SHIN DOT
<Multi_key> <U05C1> <U05BC><hebrew_shin>: "שּׁ"	UFB2C # HEBREW LETTER SHIN WITH DAGESH AND SHIN DOT
<Multi_key> <U05C2> <UFB49>		: "שּׂ"	UFB2D # HEBREW LETTER SHIN WITH DAGESH AND SIN DOT
<Multi_key> <U05C2> <U05BC><hebrew_shin>: "שּׂ"	UFB2D # HEBREW LETTER SHIN WITH DAGESH AND SIN DOT
<Multi_key> <U05B7> <hebrew_aleph>	: "אַ"	UFB2E # HEBREW LETTER ALEF WITH PATAH
<Multi_key> <U05B8> <hebrew_aleph>	: "אָ"	UFB2F # HEBREW LETTER ALEF WITH QAMATS
<Multi_key> <U05BC> <hebrew_aleph>	: "אּ"	UFB30 # HEBREW LETTER ALEF WITH MAPIQ
<Multi_key> <U05BC> <hebrew_bet>	: "בּ"	UFB31 # HEBREW LETTER BET WITH DAGESH
<Multi_key> <U05BC> <hebrew_gimel>	: "גּ"	UFB32 # HEBREW LETTER GIMEL WITH DAGESH
<Multi_key> <U05BC> <hebrew_dalet>	: "דּ"	UFB33 # HEBREW LETTER DALET WITH DAGESH
<Multi_key> <U05BC> <hebrew_he>		: "הּ"	UFB34 # HEBREW LETTER HE WITH MAPIQ
<Multi_key> <U05BC> <hebrew_waw>	: "וּ"	UFB35 # HEBREW LETTER VAV WITH DAGESH
<Multi_key> <U05BC> <hebrew_zain>	: "זּ"	UFB36 # HEBREW LETTER ZAYIN WITH DAGESH
<Multi_key> <U05BC> <hebrew_tet>	: "טּ"	UFB38 # HEBREW LETTER TET WITH DAGESH
<Multi_key> <U05BC> <hebrew_yod>	: "יּ"	UFB39 # HEBREW LETTER YOD WITH DAGESH
<Multi_key> <U05BC> <hebrew_finalkaph>	: "ךּ"	UFB3A # HEBREW LETTER FINAL KAF WITH DAGESH
<Multi_key> <U05BC> <hebrew_kaph>	: "כּ"	UFB3B # HEBREW LETTER KAF WITH DAGESH
<Multi_key> <U05BC> <hebrew_lamed>	: "לּ"	UFB3C # HEBREW LETTER LAMED WITH DAGESH
<Multi_key> <U05BC> <hebrew_mem>	: "מּ"	UFB3E # HEBREW LETTER MEM WITH DAGESH
<Multi_key> <U05BC> <hebrew_nun>	: "נּ"	UFB40 # HEBREW LETTER NUN WITH DAGESH
<Multi_key> <U05BC> <hebrew_samech>	: "סּ"	UFB41 # HEBREW LETTER SAMEKH WITH DAGESH
<Multi_key> <U05BC> <hebrew_finalpe>	: "ףּ"	UFB43 # HEBREW LETTER FINAL PE WITH DAGESH
<Multi_key> <U05BC> <hebrew_pe>		: "פּ"	UFB44 # HEBREW LETTER PE WITH DAGESH
<Multi_key> <U05BC> <hebrew_zade>	: "צּ"	UFB46 # HEBREW LETTER TSADI WITH DAGESH
<Multi_key> <U05BC> <hebrew_qoph>	: "קּ"	UFB47 # HEBREW LETTER QOF WITH DAGESH
<Multi_key> <U05BC> <hebrew_resh>	: "רּ"	UFB48 # HEBREW LETTER RESH WITH DAGESH
<Multi_key> <U05BC> <hebrew_shin>	: "שּ"	UFB49 # HEBREW LETTER SHIN WITH DAGESH
<Multi_key> <U05BC> <hebrew_taw>	: "תּ"	UFB4A # HEBREW LETTER TAV WITH DAGESH
<Multi_key> <U05B9> <hebrew_waw>	: "וֹ"	UFB4B # HEBREW LETTER VAV WITH HOLAM
<Multi_key> <U05BF> <hebrew_bet>	: "בֿ"	UFB4C # HEBREW LETTER BET WITH RAFE
<Multi_key> <U05BF> <hebrew_kaph>	: "כֿ"	UFB4D # HEBREW LETTER KAF WITH RAFE
<Multi_key> <U05BF> <hebrew_pe>		: "פֿ"	UFB4E # HEBREW LETTER PE WITH RAFE
# Musical notes
<Multi_key> <U1D157> <U1D165>		: "𝅗𝅥"	U1D15E # MUSICAL SYMBOL HALF NOTE
<Multi_key> <U1D158> <U1D165>		: "𝅘𝅥"	U1D15F # MUSICAL SYMBOL QUARTER NOTE
<Multi_key> <U1D15F> <U1D16E>		: "𝅘𝅥𝅮"	U1D160 # MUSICAL SYMBOL EIGHTH NOTE
<Multi_key> <U1D15F> <U1D16F>		: "𝅘𝅥𝅯"	U1D161 # MUSICAL SYMBOL SIXTEENTH NOTE
<Multi_key> <U1D15F> <U1D170>		: "𝅘𝅥𝅰"	U1D162 # MUSICAL SYMBOL THIRTY-SECOND NOTE
<Multi_key> <U1D15F> <U1D171>		: "𝅘𝅥𝅱"	U1D163 # MUSICAL SYMBOL SIXTY-FOURTH NOTE
<Multi_key> <U1D15F> <U1D172>		: "𝅘𝅥𝅲"	U1D164 # MUSICAL SYMBOL ONE HUNDRED TWENTY-EIGHTH NOTE
<Multi_key> <U1D1B9> <U1D165>		: "𝆹𝅥"	U1D1BB # MUSICAL SYMBOL MINIMA
<Multi_key> <U1D1BA> <U1D165>		: "𝆺𝅥"	U1D1BC # MUSICAL SYMBOL MINIMA BLACK
<Multi_key> <U1D1BB> <U1D16E>		: "𝆹𝅥𝅮"	U1D1BD # MUSICAL SYMBOL SEMIMINIMA WHITE
<Multi_key> <U1D1BC> <U1D16E>		: "𝆺𝅥𝅮"	U1D1BE # MUSICAL SYMBOL SEMIMINIMA BLACK
<Multi_key> <U1D1BB> <U1D16F>		: "𝆹𝅥𝅯"	U1D1BF # MUSICAL SYMBOL FUSA WHITE
<Multi_key> <U1D1BC> <U1D16F>		: "𝆺𝅥𝅯"	U1D1C0 # MUSICAL SYMBOL FUSA BLACK
# Khmer digraphs
<U17ff>	: "ាំ"	# KHMER VOWEL SIGN AA plus KHMER SIGN NIKAHIT
<U17fe>	: "ោះ"	# KHMER VOWEL SIGN OO plus KHMER SIGN REAHMUK
<U17fd>	: "េះ"	# KHMER VOWEL SIGN E plus KHMER SIGN REAHMUK
<U17fc>	: "ុំ"	# KHMER VOWEL SIGN U plus KHMER SIGN NIKAHIT
<U17fb>	: "ុះ"	# KHMER VOWEL SIGN U plus KHMER SIGN REAHMUK
# Decomposition of four Arabic Lam-Alef ligatures
<UFEFB>	: "لا"	# ARABIC LETTER LAM plus ARABIC LETTER ALEF
<UFEF7>	: "لأ"	# ARABIC LETTER LAM plus ARABIC LETTER ALEF WITH HAMZA ABOVE
<UFEF9>	: "لإ"	# ARABIC LETTER LAM plus ARABIC LETTER ALEF WITH HAMZA BELOW
<UFEF5>	: "لآ"	# ARABIC LETTER LAM plus ARABIC LETTER ALEF WITH MADDA ABOVE
# Breton N-graphs
<ch>	: "ch"	# LATIN SMALL LETTER C plus LATIN SMALL LETTER H
<Ch>	: "Ch"	# LATIN CAPITAL LETTER C plus LATIN SMALL LETTER H
<CH>	: "CH"	# LATIN CAPITAL LETTER C plus LATIN CAPITAL LETTER H
<c_h>	: "c’h"	# LATIN SMALL LETTER C plus RIGHT SINGLE QUOTATION MARK plus LATIN SMALL LETTER H
<C_h>	: "C’h"	# LATIN CAPITAL LETTER C plus RIGHT SINGLE QUOTATION MARK plus LATIN SMALL LETTER H
<C_H>	: "C’H"	# LATIN CAPITAL LETTER C plus RIGHT SINGLE QUOTATION MARK plus LATIN CAPITAL LETTER H
# French-Dvorak Bépo compositions
<dead_abovedot> <j>			: "ȷ"	U0237 # LATIN SMALL LETTER DOTLESS J
<dead_abovedot> <L>			: "Ŀ"	U013F # LATIN CAPITAL LETTER L WITH MIDDLE DOT
<dead_abovedot> <l>			: "ŀ"	U0140 # LATIN SMALL LETTER L WITH MIDDLE DOT
<dead_abovedot> <nobreakspace>		: "̇"	U0307 #  COMBINING DOT ABOVE
<dead_abovering> <Aacute>		: "Ǻ"	U01FA # LATIN CAPITAL LETTER A WITH RING ABOVE AND ACUTE
<dead_abovering> <aacute>		: "ǻ"	U01FB # LATIN SMALL LETTER A WITH RING ABOVE AND ACUTE
<dead_abovering> <nobreakspace>		: "̊"	U030A # COMBINING RING ABOVE
<dead_acute> <V>			: "Ǘ"	U01D7 # LATIN CAPITAL LETTER U WITH DIAERESIS AND ACUTE
<dead_acute> <v>			: "ǘ"	U01D8 # LATIN SMALL LETTER U WITH DIAERESIS AND ACUTE
<dead_acute> <nobreakspace>		: "́"	U0301 # COMBINING ACUTE ACCENT
<dead_belowdot> <dead_belowdot>		: "̣"	U0323 # COMBINING DOT BELOW
<dead_belowdot> <nobreakspace>		: "̣"	U0323 # COMBINING DOT BELOW
<dead_belowdot> <space>			: "̣"	U0323 # COMBINING DOT BELOW
<dead_breve> <Aacute>			: "Ắ"	Abreveacute # LATIN CAPITAL LETTER A WITH BREVE AND ACUTE
<dead_breve> <aacute>			: "ắ"	abreveacute # LATIN SMALL LETTER A WITH BREVE AND ACUTE
<dead_breve> <Agrave>			: "Ằ"	Abrevegrave # LATIN CAPITAL LETTER A WITH BREVE AND GRAVE
<dead_breve> <agrave>			: "ằ"	abrevegrave # LATIN SMALL LETTER A WITH BREVE AND GRAVE
<dead_breve> <Atilde>			: "Ẵ"	Abrevetilde # LATIN CAPITAL LETTER A WITH BREVE AND TILDE
<dead_breve> <atilde>			: "ẵ"	abrevetilde # LATIN SMALL LETTER A WITH BREVE AND TILDE
<dead_breve> <nobreakspace>		: "̆"	U0306 # COMBINING BREVE
<dead_caron> <U01F2>			: "ǅ"	U01C5 # LATIN CAPITAL LETTER D WITH SMALL LETTER Z WITH CARON
<dead_caron> <V>			: "Ǚ"	U01D9 # LATIN CAPITAL LETTER U WITH DIAERESIS AND CARON
<dead_caron> <v>			: "ǚ"	U01DA # LATIN SMALL LETTER U WITH DIAERESIS AND CARON
<dead_caron> <nobreakspace>		: "̌"	U030C # COMBINING CARON
<dead_cedilla> <Cacute>			: "Ḉ"	U1E08 # LATIN CAPITAL LETTER C WITH CEDILLA AND ACUTE
<dead_cedilla> <cacute>			: "ḉ"	U1E09 # LATIN SMALL LETTER C WITH CEDILLA AND ACUTE
<dead_cedilla> <U0114>			: "Ḝ"	U1E1C # LATIN CAPITAL LETTER E WITH CEDILLA AND BREVE
<dead_cedilla> <U0115>			: "ḝ"	U1E1D # LATIN SMALL LETTER E WITH CEDILLA AND BREVE
<dead_cedilla> <nobreakspace>		: "̧"	U0327 # COMBINING CEDILLA
<dead_circumflex> <Aacute>		: "Ấ"	Acircumflexacute # LATIN CAPITAL LETTER A WITH CIRCUMFLEX AND ACUTE
<dead_circumflex> <aacute>		: "ấ"	acircumflexacute # LATIN SMALL LETTER A WITH CIRCUMFLEX AND ACUTE
<dead_circumflex> <Agrave>		: "Ầ"	Acircumflexgrave # LATIN CAPITAL LETTER A WITH CIRCUMFLEX AND GRAVE
<dead_circumflex> <agrave>		: "ầ"	acircumflexgrave # LATIN SMALL LETTER A WITH CIRCUMFLEX AND GRAVE
<dead_circumflex> <Atilde>		: "Ẫ"	Acircumflextilde # LATIN CAPITAL LETTER A WITH CIRCUMFLEX AND TILDE
<dead_circumflex> <atilde>		: "ẫ"	acircumflextilde # LATIN SMALL LETTER A WITH CIRCUMFLEX AND TILDE
<dead_circumflex> <Eacute>		: "Ế"	Ecircumflexacute # LATIN CAPITAL LETTER E WITH CIRCUMFLEX AND ACUTE
<dead_circumflex> <eacute>		: "ế"	ecircumflexacute # LATIN SMALL LETTER E WITH CIRCUMFLEX AND ACUTE
<dead_circumflex> <Egrave>		: "Ề"	Ecircumflexgrave # LATIN CAPITAL LETTER E WITH CIRCUMFLEX AND GRAVE
<dead_circumflex> <egrave>		: "ề"	ecircumflexgrave # LATIN SMALL LETTER E WITH CIRCUMFLEX AND GRAVE
<dead_circumflex> <Etilde>		: "Ễ"	Ecircumflextilde # LATIN CAPITAL LETTER E WITH CIRCUMFLEX AND TILDE
<dead_circumflex> <etilde>		: "ễ"	ecircumflextilde # LATIN SMALL LETTER E WITH CIRCUMFLEX AND TILDE
<dead_circumflex> <Oacute>		: "Ố"	Ocircumflexacute # LATIN CAPITAL LETTER O WITH CIRCUMFLEX AND ACUTE
<dead_circumflex> <oacute>		: "ố"	ocircumflexacute # LATIN SMALL LETTER O WITH CIRCUMFLEX AND ACUTE
<dead_circumflex> <Ograve>		: "Ồ"	Ocircumflexgrave # LATIN CAPITAL LETTER O WITH CIRCUMFLEX AND GRAVE
<dead_circumflex> <ograve>		: "ồ"	ocircumflexgrave # LATIN SMALL LETTER O WITH CIRCUMFLEX AND GRAVE
<dead_circumflex> <Otilde>		: "Ỗ"	Ocircumflextilde # LATIN CAPITAL LETTER O WITH CIRCUMFLEX AND TILDE
<dead_circumflex> <otilde>		: "ỗ"	ocircumflextilde # LATIN SMALL LETTER O WITH CIRCUMFLEX AND TILDE
<dead_circumflex> <nobreakspace>	: "̂"	U0302 # COMBINING CIRCUMFLEX ACCENT
<dead_belowcomma> <dead_belowcomma>	: ","	comma # COMMA
<dead_belowcomma> <nobreakspace>	: "̦"	U0326 # COMBINING COMMA BELOW
<dead_belowcomma> <space>		: ","	comma # COMMA
<dead_currency> <A>			: "₳"	U20B3 # AUSTRAL SIGN
<dead_currency> <a>			: "؋"	U060B # AFGHANI SIGN
<dead_currency> <B>			: "₱"	U20B1 # PESO SIGN
<dead_currency> <b>			: "฿"	Thai_baht # THAI CURRENCY SYMBOL BAHT
<dead_currency> <C>			: "₡"	ColonSign # COLON SIGN
<dead_currency> <c>			: "¢"	cent # CENT SIGN
<dead_currency> <Ccedilla>		: "₵"	U20B5 # CEDI SIGN
<dead_currency> <ccedilla>		: "₵"	U20B5 # CEDI SIGN
<dead_currency> <dead_cedilla> <C>	: "₵"	U20B5 # CEDI SIGN
<dead_currency> <dead_cedilla> <c>	: "₵"	U20B5 # CEDI SIGN
<dead_currency> <D>			: "₯"	U20AF # DRACHMA SIGN
<dead_currency> <d>			: "₫"	DongSign # DONG SIGN
<dead_currency> <E>			: "₠"	EcuSign # EURO-CURRENCY SIGN
<dead_currency> <e>			: "€"	EuroSign # EURO SIGN
<dead_currency> <F>			: "₣"	FFrancSign # FRENCH FRANC SIGN
<dead_currency> <f>			: "ƒ"	function # LATIN SMALL LETTER F WITH HOOK
<dead_currency> <G>			: "₲"	U20B2 # GUARANI SIGN
<dead_currency> <g>			: "₲"	U20B2 # GUARANI SIGN
<dead_currency> <H>			: "₴"	U20B4 # HRYVNIA SIGN
<dead_currency> <h>			: "₴"	U20B4 # HRYVNIA SIGN
<dead_currency> <I>			: "៛"	U17DB # KHMER CURRENCY SYMBOL RIEL
<dead_currency> <i>			: "﷼"	UFDFC # RIAL SIGN
<dead_currency> <K>			: "₭"	U20AD # KIP SIGN
<dead_currency> <k>			: "₭"	U20AD # KIP SIGN
<dead_currency> <L>			: "₤"	LiraSign # LIRA SIGN
<dead_currency> <l>			: "£"	sterling # POUND SIGN
<dead_currency> <M>			: "ℳ"	U2133 # SCRIPT CAPITAL M
<dead_currency> <m>			: "₥"	MillSign # MILL SIGN
<dead_currency> <N>			: "₦"	NairaSign # NAIRA SIGN
<dead_currency> <n>			: "₦"	NairaSign # NAIRA SIGN
<dead_currency> <O>			: "૱"	U0AF1 # GUJARATI RUPEE SIGN
<dead_currency> <o>			: "௹"	U0BF9 # TAMIL RUPEE SIGN
<dead_currency> <P>			: "₧"	PesetaSign # PESETA SIGN
<dead_currency> <p>			: "₰"	U20B0 # GERMAN PENNY SIGN
<dead_currency> <r>			: "₢"	CruzeiroSign # CRUZEIRO SIGN
<dead_currency> <R>			: "₨"	RupeeSign # RUPEE SIGN
<dead_currency> <S>			: "$"	dollar # DOLLAR SIGN
<dead_currency> <s>			: "₪"	NewSheqelSign # NEW SHEQEL SIGN
<dead_currency> <T>			: "₮"	U20AE # TUGRIK SIGN
<dead_currency> <t>			: "৳"	U09F3 # BENGALI RUPEE SIGN
<dead_currency> <THORN>			: "৲"	U09F2 # BENGALI RUPEE MARK
<dead_currency> <thorn>			: "৲"	U09F2 # BENGALI RUPEE MARK
<dead_currency> <U>			: "圓"	U5713 # YUAN / WEN
<dead_currency> <u>			: "元"	U5143 # YUAN / WEN
<dead_currency> <W>			: "₩"	WonSign # WON SIGN
<dead_currency> <w>			: "₩"	WonSign # WON SIGN
<dead_currency> <Y>			: "円"	U5186 # YEN
<dead_currency> <y>			: "¥"	yen # YEN SIGN
<dead_currency> <dead_currency>		: "¤"	currency # CURRENCY SIGN
<dead_currency> <nobreakspace>		: "¤"	currency # CURRENCY SIGN
<dead_currency> <space>			: "¤"	currency # CURRENCY SIGN
<dead_diaeresis> <Iacute>		: "Ḯ"	U1E2E # LATIN CAPITAL LETTER I WITH DIAERESIS AND ACUTE
<dead_diaeresis> <iacute>		: "ḯ"	U1E2F # LATIN SMALL LETTER I WITH DIAERESIS AND ACUTE
<dead_diaeresis> <Uacute>		: "Ǘ"	U01D7 # LATIN CAPITAL LETTER U WITH DIAERESIS AND ACUTE
<dead_diaeresis> <uacute>		: "ǘ"	U01D8 # LATIN SMALL LETTER U WITH DIAERESIS AND ACUTE
<dead_diaeresis> <Ugrave>		: "Ǜ"	U01DB # LATIN CAPITAL LETTER U WITH DIAERESIS AND GRAVE
<dead_diaeresis> <ugrave>		: "ǜ"	U01DC # LATIN SMALL LETTER U WITH DIAERESIS AND GRAVE
<dead_diaeresis> <nobreakspace>		: "̈"	U0308 # COMBINING DIAERESIS
<dead_doubleacute> <nobreakspace>	: "̋"	U030B # COMBINING DOUBLE ACUTE ACCENT
<dead_grave> <V>			: "Ǜ"	U01DB # LATIN CAPITAL LETTER U WITH DIAERESIS AND GRAVE
<dead_grave> <v>			: "ǜ"	U01DC # LATIN SMALL LETTER U WITH DIAERESIS AND GRAVE
<dead_grave> <nobreakspace>		: "̀"	U0300 # COMBINING GRAVE ACCENT
<dead_greek> <A>			: "Α"	U0391 # GREEK CAPITAL LETTER ALPHA
<dead_greek> <a>			: "α"	U03B1 # GREEK SMALL LETTER ALPHA
<dead_greek> <B>			: "Β"	U0392 # GREEK CAPITAL LETTER BETA
<dead_greek> <b>			: "β"	U03B2 # GREEK SMALL LETTER BETA
<dead_greek> <D>			: "Δ"	U0394 # GREEK CAPITAL LETTER DELTA
<dead_greek> <d>			: "δ"	U03B4 # GREEK SMALL LETTER DELTA
<dead_greek> <E>			: "Ε"	U0395 # GREEK CAPITAL LETTER EPSILON
<dead_greek> <e>			: "ε"	U03B5 # GREEK SMALL LETTER EPSILON
<dead_greek> <F>			: "Φ"	U03A6 # GREEK CAPITAL LETTER PHI
<dead_greek> <f>			: "φ"	U03C6 # GREEK SMALL LETTER PHI
<dead_greek> <G>			: "Γ"	U0393 # GREEK CAPITAL LETTER GAMMA
<dead_greek> <g>			: "γ"	U03B3 # GREEK SMALL LETTER GAMMA
<dead_greek> <H>			: "Η"	U0397 # GREEK CAPITAL LETTER ETA
<dead_greek> <h>			: "η"	U03B7 # GREEK SMALL LETTER ETA
<dead_greek> <I>			: "Ι"	U0399 # GREEK CAPITAL LETTER IOTA
<dead_greek> <i>			: "ι"	U03B9 # GREEK SMALL LETTER IOTA
<dead_greek> <J>			: "Θ"	U0398 # GREEK CAPITAL LETTER THETA
<dead_greek> <j>			: "θ"	U03B8 # GREEK SMALL LETTER THETA
<dead_greek> <K>			: "Κ"	U039A # GREEK CAPITAL LETTER KAPPA
<dead_greek> <k>			: "κ"	U03BA # GREEK SMALL LETTER KAPPA
<dead_greek> <L>			: "Λ"	U039B # GREEK CAPITAL LETTER LAMDA
<dead_greek> <l>			: "λ"	U03BB # GREEK SMALL LETTER LAMDA
<dead_greek> <M>			: "Μ"	U039C # GREEK CAPITAL LETTER MU
<dead_greek> <m>			: "μ"	U03BC # GREEK SMALL LETTER MU
<dead_greek> <N>			: "Ν"	U039D # GREEK CAPITAL LETTER NU
<dead_greek> <n>			: "ν"	U03BD # GREEK SMALL LETTER NU
<dead_greek> <O>			: "Ο"	U039F # GREEK CAPITAL LETTER OMICRON
<dead_greek> <o>			: "ο"	U03BF # GREEK SMALL LETTER OMICRON
<dead_greek> <P>			: "Π"	U03A0 # GREEK CAPITAL LETTER PI
<dead_greek> <p>			: "π"	U03C0 # GREEK SMALL LETTER PI
<dead_greek> <Q>			: "Χ"	U03A7 # GREEK CAPITAL LETTER CHI
<dead_greek> <q>			: "χ"	U03C7 # GREEK SMALL LETTER CHI
<dead_greek> <R>			: "Ρ"	U03A1 # GREEK CAPITAL LETTER RHO
<dead_greek> <r>			: "ρ"	U03C1 # GREEK SMALL LETTER RHO
<dead_greek> <S>			: "Σ"	U03A3 # GREEK CAPITAL LETTER SIGMA
<dead_greek> <s>			: "σ"	U03C3 # GREEK SMALL LETTER SIGMA
<dead_greek> <T>			: "Τ"	U03A4 # GREEK CAPITAL LETTER TAU
<dead_greek> <t>			: "τ"	U03C4 # GREEK SMALL LETTER TAU
<dead_greek> <U>			: "Υ"	U03A5 # GREEK CAPITAL LETTER UPSILON
<dead_greek> <u>			: "υ"	U03C5 # GREEK SMALL LETTER UPSILON
<dead_greek> <W>			: "Ω"	U03A9 # GREEK CAPITAL LETTER OMEGA
<dead_greek> <w>			: "ω"	U03C9 # GREEK SMALL LETTER OMEGA
<dead_greek> <X>			: "Ξ"	U039E # GREEK CAPITAL LETTER XI
<dead_greek> <x>			: "ξ"	U03BE # GREEK SMALL LETTER XI
<dead_greek> <Y>			: "Ψ"	U03A8 # GREEK CAPITAL LETTER PSI
<dead_greek> <y>			: "ψ"	U03C8 # GREEK SMALL LETTER PSI
<dead_greek> <Z>			: "Ζ"	U0396 # GREEK CAPITAL LETTER ZETA
<dead_greek> <z>			: "ζ"	U03B6 # GREEK SMALL LETTER ZETA
<dead_greek> <dead_greek>		: "µ"	U00B5 # MICRO SIGN
<dead_greek> <nobreakspace>		: "µ"	U00B5 # MICRO SIGN
<dead_greek> <space>			: "µ"	U00B5 # MICRO SIGN
<dead_hook> <B>				: "Ɓ"	U0181 # LATIN CAPITAL LETTER B WITH HOOK
<dead_hook> <b>				: "ɓ"	U0253 # LATIN SMALL LETTER B WITH HOOK
<dead_hook> <C>				: "Ƈ"	U0187 # LATIN CAPITAL LETTER C WITH HOOK
<dead_hook> <c>				: "ƈ"	U0188 # LATIN SMALL LETTER C WITH HOOK
<dead_hook> <D>				: "Ɗ"	U018A # LATIN CAPITAL LETTER D WITH HOOK
<dead_hook> <d>				: "ɗ"	U0257 # LATIN SMALL LETTER D WITH HOOK
<dead_hook> <F>				: "Ƒ"	U0191 # LATIN CAPITAL LETTER F WITH HOOK
<dead_hook> <f>				: "ƒ"	function # LATIN SMALL LETTER F WITH HOOK
<dead_hook> <G>				: "Ɠ"	U0193 # LATIN CAPITAL LETTER G WITH HOOK
<dead_hook> <g>				: "ɠ"	U0260 # LATIN SMALL LETTER G WITH HOOK
<dead_hook> <h>				: "ɦ"	U0266 # LATIN SMALL LETTER H WITH HOOK
<dead_hook> <K>				: "Ƙ"	U0198 # LATIN CAPITAL LETTER K WITH HOOK
<dead_hook> <k>				: "ƙ"	U0199 # LATIN SMALL LETTER K WITH HOOK
<dead_hook> <M>				: "Ɱ"	U2C6E # LATIN CAPITAL LETTER M WITH HOOK
<dead_hook> <m>				: "ɱ"	U0271 # LATIN SMALL LETTER M WITH HOOK
<dead_hook> <N>				: "Ɲ"	U019D # LATIN CAPITAL LETTER N WITH LEFT HOOK
<dead_hook> <n>				: "ɲ"	U0272 # LATIN SMALL LETTER N WITH LEFT HOOK
<dead_hook> <P>				: "Ƥ"	U01A4 # LATIN CAPITAL LETTER P WITH HOOK
<dead_hook> <p>				: "ƥ"	U01A5 # LATIN SMALL LETTER P WITH HOOK
<dead_hook> <q>				: "ʠ"	U02A0 # LATIN SMALL LETTER Q WITH HOOK
<dead_hook> <r>				: "ɼ"	U027C # LATIN SMALL LETTER R WITH LONG LEG
<dead_hook> <s>				: "ʂ"	U0282 # LATIN SMALL LETTER S WITH HOOK
<dead_hook> <schwa>			: "ɚ"	U025A # LATIN SMALL LETTER SCHWA WITH HOOK
<dead_hook> <T>				: "Ƭ"	U01AC # LATIN CAPITAL LETTER T WITH HOOK
<dead_hook> <t>				: "ƭ"	U01AD # LATIN SMALL LETTER T WITH HOOK
<dead_hook> <V>				: "Ʋ"	U01B2 # LATIN CAPITAL LETTER V WITH HOOK
<dead_hook> <v>				: "ʋ"	U028B # LATIN SMALL LETTER V WITH HOOK
<dead_hook> <W>				: "Ⱳ"	U2C72 # LATIN CAPITAL LETTER W WITH HOOK
<dead_hook> <w>				: "ⱳ"	U2C73 # LATIN SMALL LETTER W WITH HOOK
<dead_hook> <Z>				: "Ȥ"	U0224 # LATIN CAPITAL LETTER Z WITH HOOK
<dead_hook> <z>				: "ȥ"	U0225 # LATIN SMALL LETTER Z WITH HOOK
<dead_hook> <dead_hook>			: "̉"	U0309 # COMBINING HOOK ABOVE
<dead_hook> <nobreakspace>		: "̉"	U0309 # COMBINING HOOK ABOVE
<dead_hook> <space>			: "̉"	U0309 # COMBINING HOOK ABOVE
<dead_horn> <Oacute>			: "Ớ"	Ohornacute # LATIN CAPITAL LETTER O WITH HORN AND ACUTE
<dead_horn> <oacute>			: "ớ"	ohornacute # LATIN SMALL LETTER O WITH HORN AND ACUTE
<dead_horn> <Ograve>			: "Ờ"	Ohorngrave # LATIN CAPITAL LETTER O WITH HORN AND GRAVE
<dead_horn> <ograve>			: "ờ"	ohorngrave # LATIN SMALL LETTER O WITH HORN AND GRAVE
<dead_horn> <Uacute>			: "Ứ"	Uhornacute # LATIN CAPITAL LETTER U WITH HORN AND ACUTE
<dead_horn> <uacute>			: "ứ"	uhornacute # LATIN SMALL LETTER U WITH HORN AND ACUTE
<dead_horn> <Ugrave>			: "Ừ"	Uhorngrave # LATIN CAPITAL LETTER U WITH HORN AND GRAVE
<dead_horn> <ugrave>			: "ừ"	uhorngrave # LATIN SMALL LETTER U WITH HORN AND GRAVE
<dead_horn> <dead_horn>			: "̛"	U031B # COMBINING HORN
<dead_horn> <nobreakspace>		: "̛"	U031B # COMBINING HORN
<dead_horn> <space>			: "̛"	U031B # COMBINING HORN
<dead_macron> <Eacute>			: "Ḗ"	U1E16 # LATIN CAPITAL LETTER E WITH MACRON AND ACUTE
<dead_macron> <eacute>			: "ḗ"	U1E17 # LATIN SMALL LETTER E WITH MACRON AND ACUTE
<dead_macron> <Egrave>			: "Ḕ"	U1E14 # LATIN CAPITAL LETTER E WITH MACRON AND GRAVE
<dead_macron> <egrave>			: "ḕ"	U1E15 # LATIN SMALL LETTER E WITH MACRON AND GRAVE
<dead_macron> <Oacute>			: "Ṓ"	U1E52 # LATIN CAPITAL LETTER O WITH MACRON AND ACUTE
<dead_macron> <oacute>			: "ṓ"	U1E53 # LATIN SMALL LETTER O WITH MACRON AND ACUTE
<dead_macron> <Ograve>			: "Ṑ"	U1E50 # LATIN CAPITAL LETTER O WITH MACRON AND GRAVE
<dead_macron> <ograve>			: "ṑ"	U1E51 # LATIN SMALL LETTER O WITH MACRON AND GRAVE
<dead_macron> <V>			: "Ǖ"	U01D5 # LATIN CAPITAL LETTER U WITH DIAERESIS AND MACRON
<dead_macron> <v>			: "ǖ"	U01D6 # LATIN SMALL LETTER U WITH DIAERESIS AND MACRON
<dead_macron> <nobreakspace>		: "̄"	U0304 # COMBINING MACRON
<dead_ogonek> <nobreakspace>		: "̨"	U0328 # COMBINING OGONEK
<dead_stroke> <2>			: "ƻ"	U01BB # LATIN LETTER TWO WITH STROKE
<dead_stroke> <equal>			: "≠"	notequal # NOT EQUAL TO
<dead_stroke> <A>			: "Ⱥ"	U023A # LATIN CAPITAL LETTER A WITH STROKE
<dead_stroke> <a>			: "ⱥ"	U2C65 # LATIN SMALL LETTER A WITH STROKE
<dead_stroke> <C>			: "Ȼ"	U023B # LATIN CAPITAL LETTER C WITH STROKE
<dead_stroke> <c>			: "ȼ"	U023C # LATIN SMALL LETTER C WITH STROKE
<dead_stroke> <E>			: "Ɇ"	U0246 # LATIN CAPITAL LETTER E WITH STROKE
<dead_stroke> <e>			: "ɇ"	U0247 # LATIN SMALL LETTER E WITH STROKE
<dead_stroke> <greater>			: "≯"	U226F # NOT GREATER-THAN
<dead_stroke> <greaterthanequal>	: "≱"	U2271 # NEITHER GREATER-THAN NOR EQUAL TO
<dead_stroke> <J>			: "Ɉ"	U0248 # LATIN CAPITAL LETTER J WITH STROKE
<dead_stroke> <j>			: "ɉ"	U0249 # LATIN SMALL LETTER J WITH STROKE
<dead_stroke> <U0269>			: "ᵼ"	U1D7C # LATIN SMALL LETTER IOTA WITH STROKE
<dead_stroke> <U0237>			: "ɟ"	U025F # LATIN SMALL LETTER DOTLESS J WITH STROKE
<dead_stroke> <less>			: "≮"	U226E # NOT LESS-THAN
<dead_stroke> <lessthanequal>		: "≰"	U2270 # NEITHER LESS-THAN NOR EQUAL TO
<dead_stroke> <Oacute>			: "Ǿ"	U01FE # LATIN CAPITAL LETTER O WITH STROKE AND ACUTE
<dead_stroke> <oacute>			: "ǿ"	U01FF # LATIN SMALL LETTER O WITH STROKE AND ACUTE
<dead_stroke> <P>			: "Ᵽ"	U2C63 # LATIN CAPITAL LETTER P WITH STROKE
<dead_stroke> <p>			: "ᵽ"	U1D7D # LATIN SMALL LETTER P WITH STROKE
<dead_stroke> <R>			: "Ɍ"	U024C # LATIN CAPITAL LETTER R WITH STROKE
<dead_stroke> <r>			: "ɍ"	U024D # LATIN SMALL LETTER R WITH STROKE
<dead_stroke> <U>			: "Ʉ"	U0244 # LATIN CAPITAL LETTER U BAR
<dead_stroke> <u>			: "ʉ"	U0289 # LATIN SMALL LETTER U BAR
<dead_stroke> <Y>			: "Ɏ"	U024E # LATIN CAPITAL LETTER Y WITH STROKE
<dead_stroke> <y>			: "ɏ"	U024F # LATIN SMALL LETTER Y WITH STROKE
<dead_stroke> <dead_stroke>		: "/"	slash # SOLIDUS
<dead_stroke> <nobreakspace>		: "̸"	U0338 # COMBINING LONG SOLIDUS OVERLAY
<dead_stroke> <space>			: "/"	slash # SOLIDUS
<dead_tilde> <Oacute>			: "Ṍ"	U1E4C # LATIN CAPITAL LETTER O WITH TILDE AND ACUTE
<dead_tilde> <oacute>			: "ṍ"	U1E4D # LATIN SMALL LETTER O WITH TILDE AND ACUTE
<dead_tilde> <Odiaeresis>		: "Ṏ"	U1E4E # LATIN CAPITAL LETTER O WITH TILDE AND DIAERESIS
<dead_tilde> <odiaeresis>		: "ṏ"	U1E4F # LATIN SMALL LETTER O WITH TILDE AND DIAERESIS
<dead_tilde> <Uacute>			: "Ṹ"	U1E78 # LATIN CAPITAL LETTER U WITH TILDE AND ACUTE
<dead_tilde> <uacute>			: "ṹ"	U1E79 # LATIN SMALL LETTER U WITH TILDE AND ACUTE
<dead_tilde> <equal>			: "≃"	similarequal # ASYMPTOTICALLY EQUAL TO
<dead_tilde> <less>			: "≲"	U2272 # LESS-THAN OR EQUIVALENT TO
<dead_tilde> <greater>			: "≳"	U2273 # GREATER-THAN OR EQUIVALENT TO
<dead_tilde> <nobreakspace>		: "̃"	U0303 # COMBINING TILDE
<dead_abovedot> <dead_stroke> <j>	: "ɟ"	U025F # LATIN SMALL LETTER DOTLESS J WITH STROKE
<dead_stroke> <dead_abovedot> <j>	: "ɟ"	U025F # LATIN SMALL LETTER DOTLESS J WITH STROKE
<dead_circumflex> <dead_acute> <A>	: "Ấ"	Acircumflexacute # LATIN CAPITAL LETTER A WITH CIRCUMFLEX AND ACUTE
<dead_circumflex> <dead_acute> <a>	: "ấ"	acircumflexacute # LATIN SMALL LETTER A WITH CIRCUMFLEX AND ACUTE
<dead_circumflex> <dead_acute> <E>	: "Ế"	Ecircumflexacute # LATIN CAPITAL LETTER E WITH CIRCUMFLEX AND ACUTE
<dead_circumflex> <dead_acute> <e>	: "ế"	ecircumflexacute # LATIN SMALL LETTER E WITH CIRCUMFLEX AND ACUTE
<dead_circumflex> <dead_acute> <O>	: "Ố"	Ocircumflexacute # LATIN CAPITAL LETTER O WITH CIRCUMFLEX AND ACUTE
<dead_circumflex> <dead_acute> <o>	: "ố"	ocircumflexacute # LATIN SMALL LETTER O WITH CIRCUMFLEX AND ACUTE
<dead_horn> <dead_belowdot> <O>		: "Ợ"	Ohornbelowdot # LATIN CAPITAL LETTER O WITH HORN AND DOT BELOW
<dead_horn> <dead_belowdot> <o>		: "ợ"	ohornbelowdot # LATIN SMALL LETTER O WITH HORN AND DOT BELOW
<dead_horn> <dead_belowdot> <U>		: "Ự"	Uhornbelowdot # LATIN CAPITAL LETTER U WITH HORN AND DOT BELOW
<dead_horn> <dead_belowdot> <u>		: "ự"	uhornbelowdot # LATIN SMALL LETTER U WITH HORN AND DOT BELOW
<dead_circumflex> <dead_grave> <A>	: "Ầ"	Acircumflexgrave # LATIN CAPITAL LETTER A WITH CIRCUMFLEX AND GRAVE
<dead_circumflex> <dead_grave> <a>	: "ầ"	acircumflexgrave # LATIN SMALL LETTER A WITH CIRCUMFLEX AND GRAVE
<dead_circumflex> <dead_grave> <E>	: "Ề"	Ecircumflexgrave # LATIN CAPITAL LETTER E WITH CIRCUMFLEX AND GRAVE
<dead_circumflex> <dead_grave> <e>	: "ề"	ecircumflexgrave # LATIN SMALL LETTER E WITH CIRCUMFLEX AND GRAVE
<dead_circumflex> <dead_grave> <O>	: "Ồ"	Ocircumflexgrave # LATIN CAPITAL LETTER O WITH CIRCUMFLEX AND GRAVE
<dead_circumflex> <dead_grave> <o>	: "ồ"	ocircumflexgrave # LATIN SMALL LETTER O WITH CIRCUMFLEX AND GRAVE
<dead_circumflex> <dead_hook> <A>	: "Ẩ"	Acircumflexhook # LATIN CAPITAL LETTER A WITH CIRCUMFLEX AND HOOK ABOVE
<dead_circumflex> <dead_hook> <a>	: "ẩ"	acircumflexhook # LATIN SMALL LETTER A WITH CIRCUMFLEX AND HOOK ABOVE
<dead_circumflex> <dead_hook> <E>	: "Ể"	Ecircumflexhook # LATIN CAPITAL LETTER E WITH CIRCUMFLEX AND HOOK ABOVE
<dead_circumflex> <dead_hook> <e>	: "ể"	ecircumflexhook # LATIN SMALL LETTER E WITH CIRCUMFLEX AND HOOK ABOVE
<dead_circumflex> <dead_hook> <O>	: "Ổ"	Ocircumflexhook # LATIN CAPITAL LETTER O WITH CIRCUMFLEX AND HOOK ABOVE
<dead_circumflex> <dead_hook> <o>	: "ổ"	ocircumflexhook # LATIN SMALL LETTER O WITH CIRCUMFLEX AND HOOK ABOVE
<dead_greek> <dead_hook> <U>		: "ϒ"	U03D2 # GREEK UPSILON WITH HOOK SYMBOL
<dead_hook> <dead_greek> <U>		: "ϒ"	U03D2 # GREEK UPSILON WITH HOOK SYMBOL
<dead_greek> <dead_macron> <A>		: "Ᾱ"	U1FB9 # GREEK CAPITAL LETTER ALPHA WITH MACRON
<dead_macron> <dead_greek> <A>		: "Ᾱ"	U1FB9 # GREEK CAPITAL LETTER ALPHA WITH MACRON
<dead_greek> <dead_macron> <a>		: "ᾱ"	U1FB1 # GREEK SMALL LETTER ALPHA WITH MACRON
<dead_macron> <dead_greek> <a>		: "ᾱ"	U1FB1 # GREEK SMALL LETTER ALPHA WITH MACRON
<dead_greek> <dead_macron> <I>		: "Ῑ"	U1FD9 # GREEK CAPITAL LETTER IOTA WITH MACRON
<dead_macron> <dead_greek> <I>		: "Ῑ"	U1FD9 # GREEK CAPITAL LETTER IOTA WITH MACRON
<dead_greek> <dead_macron> <i>		: "ῑ"	U1FD1 # GREEK SMALL LETTER IOTA WITH MACRON
<dead_macron> <dead_greek> <i>		: "ῑ"	U1FD1 # GREEK SMALL LETTER IOTA WITH MACRON
<dead_greek> <dead_macron> <U>		: "Ῡ"	U1FE9 # GREEK CAPITAL LETTER UPSILON WITH MACRON
<dead_macron> <dead_greek> <U>		: "Ῡ"	U1FE9 # GREEK CAPITAL LETTER UPSILON WITH MACRON
<dead_greek> <dead_macron> <u>		: "ῡ"	U1FE1 # GREEK SMALL LETTER UPSILON WITH MACRON
<dead_macron> <dead_greek> <u>		: "ῡ"	U1FE1 # GREEK SMALL LETTER UPSILON WITH MACRON
<dead_greek> <dead_stroke> <r>		: "ϼ"	U03FC # GREEK RHO WITH STROKE SYMBOL
<dead_stroke> <dead_greek> <r>		: "ϼ"	U03FC # GREEK RHO WITH STROKE SYMBOL
# Cyrillic (NFDs -- Normalized Form Canonical Decomposition)
<dead_doublegrave> <Cyrillic_a>		: "а̏" # CYRILLIC SMALL LETTER A plus COMBINING DOUBLE GRAVE
<Multi_key> <grave><grave> <Cyrillic_a>	: "а̏" # CYRILLIC SMALL LETTER A plus COMBINING DOUBLE GRAVE
<dead_invertedbreve> <Cyrillic_a>	: "а̑" # CYRILLIC SMALL LETTER A plus COMBINING INVERTED BREVE
<dead_grave> <Cyrillic_a>		: "а̀" # CYRILLIC SMALL LETTER A plus COMBINING GRAVE
<Multi_key> <grave> <Cyrillic_a>	: "а̀" # CYRILLIC SMALL LETTER A plus COMBINING GRAVE
<dead_acute> <Cyrillic_a>		: "а́" # CYRILLIC SMALL LETTER A plus COMBINING ACUTE
<Multi_key> <acute> <Cyrillic_a>	: "а́" # CYRILLIC SMALL LETTER A plus COMBINING ACUTE
<Multi_key> <apostrophe> <Cyrillic_a>	: "а́" # CYRILLIC SMALL LETTER A plus COMBINING ACUTE
<dead_macron> <Cyrillic_a>		: "а̄" # CYRILLIC SMALL LETTER A plus COMBINING MACRON
<Multi_key> <macron> <Cyrillic_a>	: "а̄" # CYRILLIC SMALL LETTER A plus COMBINING MACRON
<Multi_key> <underscore> <Cyrillic_a>	: "а̄" # CYRILLIC SMALL LETTER A plus COMBINING MACRON
<dead_circumflex> <Cyrillic_a>		: "а̂" # CYRILLIC SMALL LETTER A plus COMBINING CIRCUMFLEX
<Multi_key> <asciicircum> <Cyrillic_a>	: "а̂" # CYRILLIC SMALL LETTER A plus COMBINING CIRCUMFLEX
<dead_doublegrave> <Cyrillic_A>		: "А̏" # CYRILLIC CAPITAL LETTER A plus COMBINING DOUBLE GRAVE
<Multi_key> <grave><grave> <Cyrillic_A>	: "А̏" # CYRILLIC CAPITAL LETTER A plus COMBINING DOUBLE GRAVE
<dead_invertedbreve> <Cyrillic_A>	: "А̑" # CYRILLIC CAPITAL LETTER A plus COMBINING INVERTED BREVE
<dead_grave> <Cyrillic_A>		: "А̀" # CYRILLIC CAPITAL LETTER A plus COMBINING GRAVE
<Multi_key> <grave> <Cyrillic_A>	: "А̀" # CYRILLIC CAPITAL LETTER A plus COMBINING GRAVE
<dead_acute> <Cyrillic_A>		: "А́" # CYRILLIC CAPITAL LETTER A plus COMBINING ACUTE
<Multi_key> <acute> <Cyrillic_A>	: "А́" # CYRILLIC CAPITAL LETTER A plus COMBINING ACUTE
<Multi_key> <apostrophe> <Cyrillic_A>	: "А́" # CYRILLIC CAPITAL LETTER A plus COMBINING ACUTE
<dead_macron> <Cyrillic_A>		: "А̄" # CYRILLIC CAPITAL LETTER A plus COMBINING MACRON
<Multi_key> <macron> <Cyrillic_A>	: "А̄" # CYRILLIC CAPITAL LETTER A plus COMBINING MACRON
<Multi_key> <underscore> <Cyrillic_A>	: "А̄" # CYRILLIC CAPITAL LETTER A plus COMBINING MACRON
<dead_circumflex> <Cyrillic_A>		: "А̂" # CYRILLIC CAPITAL LETTER A plus COMBINING CIRCUMFLEX
<Multi_key> <asciicircum> <Cyrillic_A>	: "А̂" # CYRILLIC CAPITAL LETTER A plus COMBINING CIRCUMFLEX
<dead_doublegrave> <Cyrillic_ie>	: "е̏" # CYRILLIC SMALL LETTER IE plus COMBINING DOUBLE GRAVE
<Multi_key> <grave><grave> <Cyrillic_ie>: "е̏" # CYRILLIC SMALL LETTER IE plus COMBINING DOUBLE GRAVE
<dead_invertedbreve> <Cyrillic_ie>	: "е̑" # CYRILLIC SMALL LETTER IE plus COMBINING INVERTED BREVE
<dead_acute> <Cyrillic_ie>		: "е́" # CYRILLIC SMALL LETTER IE plus COMBINING ACUTE
<Multi_key> <acute> <Cyrillic_ie>	: "е́" # CYRILLIC SMALL LETTER IE plus COMBINING ACUTE
<Multi_key> <apostrophe> <Cyrillic_ie>	: "е́" # CYRILLIC SMALL LETTER IE plus COMBINING ACUTE
<dead_macron> <Cyrillic_ie>		: "е̄" # CYRILLIC SMALL LETTER IE plus COMBINING MACRON
<Multi_key> <macron> <Cyrillic_ie>	: "е̄" # CYRILLIC SMALL LETTER IE plus COMBINING MACRON
<Multi_key> <underscore> <Cyrillic_ie>	: "е̄" # CYRILLIC SMALL LETTER IE plus COMBINING MACRON
<dead_circumflex> <Cyrillic_ie>		: "е̂" # CYRILLIC SMALL LETTER IE plus COMBINING CIRCUMFLEX
<Multi_key> <asciicircum> <Cyrillic_ie>	: "е̂" # CYRILLIC SMALL LETTER IE plus COMBINING CIRCUMFLEX
<dead_doublegrave> <Cyrillic_IE>	: "Е̏" # CYRILLIC CAPITAL LETTER IE plus COMBINING DOUBLE GRAVE
<Multi_key> <grave><grave> <Cyrillic_IE>: "Е̏" # CYRILLIC CAPITAL LETTER IE plus COMBINING DOUBLE GRAVE
<dead_invertedbreve> <Cyrillic_IE>	: "Е̑" # CYRILLIC CAPITAL LETTER IE plus COMBINING INVERTED BREVE
<dead_acute> <Cyrillic_IE>		: "Е́" # CYRILLIC CAPITAL LETTER IE plus COMBINING ACUTE
<Multi_key> <acute> <Cyrillic_IE>	: "Е́" # CYRILLIC CAPITAL LETTER IE plus COMBINING ACUTE
<Multi_key> <apostrophe> <Cyrillic_IE>	: "Е́" # CYRILLIC CAPITAL LETTER IE plus COMBINING ACUTE
<dead_macron> <Cyrillic_IE>		: "Е̄" # CYRILLIC CAPITAL LETTER IE plus COMBINING MACRON
<Multi_key> <macron> <Cyrillic_IE>	: "Е̄" # CYRILLIC CAPITAL LETTER IE plus COMBINING MACRON
<Multi_key> <underscore> <Cyrillic_IE>	: "Е̄" # CYRILLIC CAPITAL LETTER IE plus COMBINING MACRON
<dead_circumflex> <Cyrillic_IE>		: "Е̂" # CYRILLIC CAPITAL LETTER IE plus COMBINING CIRCUMFLEX
<Multi_key> <asciicircum> <Cyrillic_IE>	: "Е̂" # CYRILLIC CAPITAL LETTER IE plus COMBINING CIRCUMFLEX
<dead_doublegrave> <Cyrillic_i>		: "и̏" # CYRILLIC SMALL LETTER I plus COMBINING DOUBLE GRAVE
<Multi_key> <grave><grave> <Cyrillic_i>	: "и̏" # CYRILLIC SMALL LETTER I plus COMBINING DOUBLE GRAVE
<dead_invertedbreve> <Cyrillic_i>	: "и̑" # CYRILLIC SMALL LETTER I plus COMBINING INVERTED BREVE
<dead_acute> <Cyrillic_i>		: "и́" # CYRILLIC SMALL LETTER I plus COMBINING ACUTE
<Multi_key> <acute> <Cyrillic_i>	: "и́" # CYRILLIC SMALL LETTER I plus COMBINING ACUTE
<Multi_key> <apostrophe> <Cyrillic_i>	: "и́" # CYRILLIC SMALL LETTER I plus COMBINING ACUTE
<dead_circumflex> <Cyrillic_i>		: "и̂" # CYRILLIC SMALL LETTER I plus COMBINING CIRCUMFLEX
<Multi_key> <asciicircum> <Cyrillic_i>	: "и̂" # CYRILLIC SMALL LETTER I plus COMBINING CIRCUMFLEX
<dead_doublegrave> <Cyrillic_I>		: "И̏" # CYRILLIC CAPITAL LETTER I plus COMBINING DOUBLE GRAVE
<Multi_key> <grave><grave> <Cyrillic_I>	: "И̏" # CYRILLIC CAPITAL LETTER I plus COMBINING DOUBLE GRAVE
<dead_invertedbreve> <Cyrillic_I>	: "И̑" # CYRILLIC CAPITAL LETTER I plus COMBINING INVERTED BREVE
<dead_acute> <Cyrillic_I>		: "И́" # CYRILLIC CAPITAL LETTER I plus COMBINING ACUTE
<Multi_key> <acute> <Cyrillic_I>	: "И́" # CYRILLIC CAPITAL LETTER I plus COMBINING ACUTE
<Multi_key> <apostrophe> <Cyrillic_I>	: "И́" # CYRILLIC CAPITAL LETTER I plus COMBINING ACUTE
<dead_circumflex> <Cyrillic_I>		: "И̂" # CYRILLIC CAPITAL LETTER I plus COMBINING CIRCUMFLEX
<Multi_key> <asciicircum> <Cyrillic_I>	: "И̂" # CYRILLIC CAPITAL LETTER I plus COMBINING CIRCUMFLEX
<dead_doublegrave> <Cyrillic_o>		: "о̏" # CYRILLIC SMALL LETTER O plus COMBINING DOUBLE GRAVE
<Multi_key> <grave><grave> <Cyrillic_o>	: "о̏" # CYRILLIC SMALL LETTER O plus COMBINING DOUBLE GRAVE
<dead_invertedbreve> <Cyrillic_o>	: "о̑" # CYRILLIC SMALL LETTER O plus COMBINING INVERTED BREVE
<dead_grave> <Cyrillic_o>		: "о̀" # CYRILLIC SMALL LETTER O plus COMBINING GRAVE
<Multi_key> <grave> <Cyrillic_o>	: "о̀" # CYRILLIC SMALL LETTER O plus COMBINING GRAVE
<dead_acute> <Cyrillic_o>		: "о́" # CYRILLIC SMALL LETTER O plus COMBINING ACUTE
<Multi_key> <acute> <Cyrillic_o>	: "о́" # CYRILLIC SMALL LETTER O plus COMBINING ACUTE
<Multi_key> <apostrophe> <Cyrillic_o>	: "о́" # CYRILLIC SMALL LETTER O plus COMBINING ACUTE
<dead_macron> <Cyrillic_o>		: "о̄" # CYRILLIC SMALL LETTER O plus COMBINING MACRON
<Multi_key> <macron> <Cyrillic_o>	: "о̄" # CYRILLIC SMALL LETTER O plus COMBINING MACRON
<Multi_key> <underscore> <Cyrillic_o>	: "о̄" # CYRILLIC SMALL LETTER O plus COMBINING MACRON
<dead_circumflex> <Cyrillic_o>		: "о̂" # CYRILLIC SMALL LETTER O plus COMBINING CIRCUMFLEX
<Multi_key> <asciicircum> <Cyrillic_o>	: "о̂" # CYRILLIC SMALL LETTER O plus COMBINING CIRCUMFLEX
<dead_doublegrave> <Cyrillic_O>		: "О̏" # CYRILLIC CAPITAL LETTER O plus COMBINING DOUBLE GRAVE
<Multi_key> <grave><grave> <Cyrillic_O>	: "О̏" # CYRILLIC CAPITAL LETTER O plus COMBINING DOUBLE GRAVE
<dead_invertedbreve> <Cyrillic_O>	: "О̑" # CYRILLIC CAPITAL LETTER O plus COMBINING INVERTED BREVE
<dead_grave> <Cyrillic_O>		: "О̀" # CYRILLIC CAPITAL LETTER O plus COMBINING GRAVE
<Multi_key> <grave> <Cyrillic_O>	: "О̀" # CYRILLIC CAPITAL LETTER O plus COMBINING GRAVE
<dead_acute> <Cyrillic_O>		: "О́" # CYRILLIC CAPITAL LETTER O plus COMBINING ACUTE
<Multi_key> <acute> <Cyrillic_O>	: "О́" # CYRILLIC CAPITAL LETTER O plus COMBINING ACUTE
<Multi_key> <apostrophe> <Cyrillic_O>	: "О́" # CYRILLIC CAPITAL LETTER O plus COMBINING ACUTE
<dead_macron> <Cyrillic_O>		: "О̄" # CYRILLIC CAPITAL LETTER O plus COMBINING MACRON
<Multi_key> <macron> <Cyrillic_O>	: "О̄" # CYRILLIC CAPITAL LETTER O plus COMBINING MACRON
<Multi_key> <underscore> <Cyrillic_O>	: "О̄" # CYRILLIC CAPITAL LETTER O plus COMBINING MACRON
<dead_circumflex> <Cyrillic_O>		: "О̂" # CYRILLIC CAPITAL LETTER O plus COMBINING CIRCUMFLEX
<Multi_key> <asciicircum> <Cyrillic_O>	: "О̂" # CYRILLIC CAPITAL LETTER O plus COMBINING CIRCUMFLEX
<dead_doublegrave> <Cyrillic_u>		: "у̏" # CYRILLIC SMALL LETTER U plus COMBINING DOUBLE GRAVE
<Multi_key> <grave><grave> <Cyrillic_u>	: "у̏" # CYRILLIC SMALL LETTER U plus COMBINING DOUBLE GRAVE
<dead_invertedbreve> <Cyrillic_u>	: "у̑" # CYRILLIC SMALL LETTER U plus COMBINING INVERTED BREVE
<dead_grave> <Cyrillic_u>		: "у̀" # CYRILLIC SMALL LETTER U plus COMBINING GRAVE
<Multi_key> <grave> <Cyrillic_u>	: "у̀" # CYRILLIC SMALL LETTER U plus COMBINING GRAVE
<dead_acute> <Cyrillic_u>		: "у́" # CYRILLIC SMALL LETTER U plus COMBINING ACUTE
<Multi_key> <acute> <Cyrillic_u>	: "у́" # CYRILLIC SMALL LETTER U plus COMBINING ACUTE
<Multi_key> <apostrophe> <Cyrillic_u>	: "у́" # CYRILLIC SMALL LETTER U plus COMBINING ACUTE
<dead_circumflex> <Cyrillic_u>		: "у̂" # CYRILLIC SMALL LETTER U plus COMBINING CIRCUMFLEX
<Multi_key> <asciicircum> <Cyrillic_u>	: "у̂" # CYRILLIC SMALL LETTER U plus COMBINING CIRCUMFLEX
<dead_doublegrave> <Cyrillic_U>		: "У̏" # CYRILLIC CAPITAL LETTER U plus COMBINING DOUBLE GRAVE
<Multi_key> <grave><grave> <Cyrillic_U>	: "У̏" # CYRILLIC CAPITAL LETTER U plus COMBINING DOUBLE GRAVE
<dead_invertedbreve> <Cyrillic_U>	: "У̑" # CYRILLIC CAPITAL LETTER U plus COMBINING INVERTED BREVE
<dead_grave> <Cyrillic_U>		: "У̀" # CYRILLIC CAPITAL LETTER U plus COMBINING GRAVE
<Multi_key> <grave> <Cyrillic_U>	: "У̀" # CYRILLIC CAPITAL LETTER U plus COMBINING GRAVE
<dead_acute> <Cyrillic_U>		: "У́" # CYRILLIC CAPITAL LETTER U plus COMBINING ACUTE
<Multi_key> <acute> <Cyrillic_U>	: "У́" # CYRILLIC CAPITAL LETTER U plus COMBINING ACUTE
<Multi_key> <apostrophe> <Cyrillic_U>	: "У́" # CYRILLIC CAPITAL LETTER U plus COMBINING ACUTE
<dead_circumflex> <Cyrillic_U>		: "У̂" # CYRILLIC CAPITAL LETTER U plus COMBINING CIRCUMFLEX
<Multi_key> <asciicircum> <Cyrillic_U>	: "У̂" # CYRILLIC CAPITAL LETTER U plus COMBINING CIRCUMFLEX
<dead_doublegrave> <Cyrillic_er>	: "р̏" # CYRILLIC SMALL LETTER ER plus COMBINING DOUBLE GRAVE
<Multi_key> <grave><grave> <Cyrillic_er>: "р̏" # CYRILLIC SMALL LETTER ER plus COMBINING DOUBLE GRAVE
<dead_invertedbreve> <Cyrillic_er>	: "р̑" # CYRILLIC SMALL LETTER ER plus COMBINING INVERTED BREVE
<dead_grave> <Cyrillic_er>		: "р̀" # CYRILLIC SMALL LETTER ER plus COMBINING GRAVE
<Multi_key> <grave> <Cyrillic_er>	: "р̀" # CYRILLIC SMALL LETTER ER plus COMBINING GRAVE
<dead_acute> <Cyrillic_er>		: "р́" # CYRILLIC SMALL LETTER ER plus COMBINING ACUTE
<Multi_key> <acute> <Cyrillic_er>	: "р́" # CYRILLIC SMALL LETTER ER plus COMBINING ACUTE
<Multi_key> <apostrophe> <Cyrillic_er>	: "р́" # CYRILLIC SMALL LETTER ER plus COMBINING ACUTE
<dead_macron> <Cyrillic_er>		: "р̄" # CYRILLIC SMALL LETTER ER plus COMBINING MACRON
<Multi_key> <macron> <Cyrillic_er>	: "р̄" # CYRILLIC SMALL LETTER ER plus COMBINING MACRON
<Multi_key> <underscore> <Cyrillic_er>	: "р̄" # CYRILLIC SMALL LETTER ER plus COMBINING MACRON
<dead_circumflex> <Cyrillic_er>		: "р̂" # CYRILLIC SMALL LETTER ER plus COMBINING CIRCUMFLEX
<Multi_key> <asciicircum> <Cyrillic_er>	: "р̂" # CYRILLIC SMALL LETTER ER plus COMBINING CIRCUMFLEX
<dead_doublegrave> <Cyrillic_ER>	: "Р̏" # CYRILLIC CAPITAL LETTER ER plus COMBINING DOUBLE GRAVE
<Multi_key> <grave><grave> <Cyrillic_ER>: "Р̏" # CYRILLIC CAPITAL LETTER ER plus COMBINING DOUBLE GRAVE
<dead_invertedbreve> <Cyrillic_ER>	: "Р̑" # CYRILLIC CAPITAL LETTER ER plus COMBINING INVERTED BREVE
<dead_grave> <Cyrillic_ER>		: "Р̀" # CYRILLIC CAPITAL LETTER ER plus COMBINING GRAVE
<Multi_key> <grave> <Cyrillic_ER>	: "Р̀" # CYRILLIC CAPITAL LETTER ER plus COMBINING GRAVE
<dead_acute> <Cyrillic_ER>		: "Р́" # CYRILLIC CAPITAL LETTER ER plus COMBINING ACUTE
<Multi_key> <acute> <Cyrillic_ER>	: "Р́" # CYRILLIC CAPITAL LETTER ER plus COMBINING ACUTE
<Multi_key> <apostrophe> <Cyrillic_ER>	: "Р́" # CYRILLIC CAPITAL LETTER ER plus COMBINING ACUTE
<dead_macron> <Cyrillic_ER>		: "Р̄" # CYRILLIC CAPITAL LETTER ER plus COMBINING MACRON
<Multi_key> <macron> <Cyrillic_ER>	: "Р̄" # CYRILLIC CAPITAL LETTER ER plus COMBINING MACRON
<Multi_key> <underscore> <Cyrillic_ER>	: "Р̄" # CYRILLIC CAPITAL LETTER ER plus COMBINING MACRON
<dead_circumflex> <Cyrillic_ER>		: "Р̂" # CYRILLIC CAPITAL LETTER ER plus COMBINING CIRCUMFLEX
<Multi_key> <asciicircum> <Cyrillic_ER>	: "Р̂" # CYRILLIC CAPITAL LETTER ER plus COMBINING CIRCUMFLEX
<dead_acute> <Cyrillic_yeru>		: "ы́" # CYRILLIC SMALL LETTER YERU plus COMBINING ACUTE
<Multi_key> <acute> <Cyrillic_yeru>	: "ы́" # CYRILLIC SMALL LETTER YERU plus COMBINING ACUTE
<Multi_key> <apostrophe> <Cyrillic_yeru>: "ы́" # CYRILLIC SMALL LETTER YERU plus COMBINING ACUTE
<dead_acute> <Cyrillic_YERU>		: "Ы́" # CYRILLIC CAPITAL LETTER YERU plus COMBINING ACUTE
<Multi_key> <acute> <Cyrillic_YERU>	: "Ы́" # CYRILLIC CAPITAL LETTER YERU plus COMBINING ACUTE
<Multi_key> <apostrophe> <Cyrillic_YERU>: "Ы́" # CYRILLIC CAPITAL LETTER YERU plus COMBINING ACUTE
<dead_acute> <Cyrillic_e>		: "э́" # CYRILLIC SMALL LETTER E plus COMBINING ACUTE
<Multi_key> <acute> <Cyrillic_e>	: "э́" # CYRILLIC SMALL LETTER E plus COMBINING ACUTE
<Multi_key> <apostrophe> <Cyrillic_e>	: "э́" # CYRILLIC SMALL LETTER E plus COMBINING ACUTE
<dead_acute> <Cyrillic_E>		: "Э́" # CYRILLIC CAPITAL LETTER E plus COMBINING ACUTE
<Multi_key> <acute> <Cyrillic_E>	: "Э́" # CYRILLIC CAPITAL LETTER E plus COMBINING ACUTE
<Multi_key> <apostrophe> <Cyrillic_E>	: "Э́" # CYRILLIC CAPITAL LETTER E plus COMBINING ACUTE
<dead_acute> <Cyrillic_yu>		: "ю́" # CYRILLIC SMALL LETTER YU plus COMBINING ACUTE
<Multi_key> <acute> <Cyrillic_yu>	: "ю́" # CYRILLIC SMALL LETTER YU plus COMBINING ACUTE
<Multi_key> <apostrophe> <Cyrillic_yu>	: "ю́" # CYRILLIC SMALL LETTER YU plus COMBINING ACUTE
<dead_acute> <Cyrillic_YU>		: "Ю́" # CYRILLIC CAPITAL LETTER YU plus COMBINING ACUTE
<Multi_key> <acute> <Cyrillic_YU>	: "Ю́" # CYRILLIC CAPITAL LETTER YU plus COMBINING ACUTE
<Multi_key> <apostrophe> <Cyrillic_YU>	: "Ю́" # CYRILLIC CAPITAL LETTER YU plus COMBINING ACUTE
<dead_acute> <Cyrillic_ya>		: "я́" # CYRILLIC SMALL LETTER YA plus COMBINING ACUTE
<Multi_key> <acute> <Cyrillic_ya>	: "я́" # CYRILLIC SMALL LETTER YA plus COMBINING ACUTE
<Multi_key> <apostrophe> <Cyrillic_ya>	: "я́" # CYRILLIC SMALL LETTER YA plus COMBINING ACUTE
<dead_acute> <Cyrillic_YA>		: "Я́" # CYRILLIC CAPITAL LETTER YA plus COMBINING ACUTE
<Multi_key> <acute> <Cyrillic_YA>	: "Я́" # CYRILLIC CAPITAL LETTER YA plus COMBINING ACUTE
<Multi_key> <apostrophe> <Cyrillic_YA>	: "Я́" # CYRILLIC CAPITAL LETTER YA plus COMBINING ACUTE
# Characters from "Mathematical Operators"
<Multi_key> <v> <slash>			: "√"	U221a # v / SQUARE ROOT
<Multi_key> <slash> <v>			: "√"	U221a # / v SQUARE ROOT
<Multi_key> <8> <8>			: "∞"	U221e # 8 8 INFINITY
<Multi_key> <colon> <period>		: "∴"	U2234 # : . THEREFORE
<Multi_key> <period> <colon>		: "∵"	U2235 # . : BECAUSE
<Multi_key> <asciitilde> <asciitilde>	: "≈"	U2248 # ~ ~ ALMOST EQUAL TO
<Multi_key> <dead_tilde> <dead_tilde>	: "≈"	U2248 # ~ ~ ALMOST EQUAL TO
<Multi_key> <equal> <underscore>	: "≡"	U2261 # = _ IDENTICAL TO
<Multi_key> <underscore> <U2260>	: "≢"	U2262 # _ ≠ NOT IDENTICAL TO
<Multi_key> <U2260> <underscore>	: "≢"	U2262 # ≠ _ NOT IDENTICAL TO
<Multi_key> <less> <underscore>		: "≤"	U2264 # < _ LESS-THAN OR EQUAL TO
<Multi_key> <underscore> <less>		: "≤"	U2264 # _ < LESS-THAN OR EQUAL TO
<Multi_key> <greater> <underscore>	: "≥"	U2265 # > _ GREATER-THAN OR EQUAL TO
<Multi_key> <underscore> <greater>	: "≥"	U2265 # _ > GREATER-THAN OR EQUAL TO
<Multi_key> <underscore> <U2282>	: "⊆"	U2286 # _ ⊂ SUBSET OF OR EQUAL TO
<Multi_key> <U2282> <underscore>	: "⊆"	U2286 # ⊂ _ SUBSET OF OR EQUAL TO
<Multi_key> <underscore> <U2283>	: "⊇"	U2287 # _ ⊃ SUPERSET OF OR EQUAL TO
<Multi_key> <U2283> <underscore>	: "⊇"	U2287 # ⊃ _ SUPERSET OF OR EQUAL TO
<Multi_key> <U25cb> <minus>		: "⊖"	U2296 # ○ - CIRCLED MINUS
<Multi_key> <minus> <U25cb>		: "⊖"	U2296 # - ○ CIRCLED MINUS
<Multi_key> <U25cb> <period>		: "⊙"	U2299 # ○ . CIRCLED DOT OPERATOR
<Multi_key> <period> <U25cb>		: "⊙"	U2299 # . ○ CIRCLED DOT OPERATOR
<Multi_key> <less> <greater>		: "⋄"	U22c4 # < > DIAMOND OPERATOR
<Multi_key> <greater> <less>		: "⋄"	U22c4 # > < DIAMOND OPERATOR
<Multi_key> <U2227> <U2228>		: "⋄"	U22c4 # ∧ ∨ DIAMOND OPERATOR
<Multi_key> <U2228> <U2227>		: "⋄"	U22c4 # ∨ ∧ DIAMOND OPERATOR
# Characters from "Miscellaneous Technical"
<Multi_key> <U22a5> <U22a4>		: "⌶"	U2336 # ⊥ ⊤ APL FUNCTIONAL SYMBOL I-BEAM
<Multi_key> <U22a4> <U22a5>		: "⌶"	U2336 # ⊥ ⊤ APL FUNCTIONAL SYMBOL I-BEAM
<Multi_key> <bracketleft> <bracketright>: "⌷"	U2337 # [ ] APL FUNCTIONAL SYMBOL SQUISH QUAD
<Multi_key> <bracketright> <bracketleft>: "⌷"	U2337 # ] [ APL FUNCTIONAL SYMBOL SQUISH QUAD
<Multi_key> <U2395> <equal>		: "⌸"	U2338 # ⎕ = APL FUNCTIONAL SYMBOL QUAD EQUAL
<Multi_key> <equal> <U2395>		: "⌸"	U2338 # = ⎕ APL FUNCTIONAL SYMBOL QUAD EQUAL
<Multi_key> <U2395> <division>		: "⌹"	U2339 # ⎕ ÷ APL FUNCTIONAL SYMBOL QUAD DIVIDE
<Multi_key> <division> <U2395>		: "⌹"	U2339 # ÷ ⎕ APL FUNCTIONAL SYMBOL QUAD DIVIDE
<Multi_key> <U2395> <U22c4>		: "⌺"	U233a # ⎕ ⋄ APL FUNCTIONAL SYMBOL QUAD DIAMOND
<Multi_key> <U22c4> <U2395>		: "⌺"	U233a # ⋄ ⎕ APL FUNCTIONAL SYMBOL QUAD DIAMOND
<Multi_key> <U2395> <U2218>		: "⌻"	U233b # ⎕ ∘ APL FUNCTIONAL SYMBOL QUAD JOT
<Multi_key> <U2218> <U2395>		: "⌻"	U233b # ∘ ⎕ APL FUNCTIONAL SYMBOL QUAD JOT
<Multi_key> <U2395> <U25cb>		: "⌼"	U233c # ⎕ ○ APL FUNCTIONAL SYMBOL QUAD CIRCLE
<Multi_key> <U25cb> <U2395>		: "⌼"	U233c # ○ ⎕ APL FUNCTIONAL SYMBOL QUAD CIRCLE
<Multi_key> <U25cb> <bar>		: "⌽"	U233d # ○ | APL FUNCTIONAL SYMBOL CIRCLE STILE
<Multi_key> <bar> <U25cb>		: "⌽"	U233d # | ○ APL FUNCTIONAL SYMBOL CIRCLE STILE
<Multi_key> <U25cb> <U2218>		: "⌾"	U233e # ○ ∘ APL FUNCTIONAL SYMBOL CIRCLE JOT
<Multi_key> <U2218> <U25cb>		: "⌾"	U233e # ∘ ○ APL FUNCTIONAL SYMBOL CIRCLE JOT
<Multi_key> <slash> <minus>		: "⌿"	U233f # / - APL FUNCTIONAL SYMBOL SLASH BAR
<Multi_key> <minus> <slash>		: "⌿"	U233f # - / APL FUNCTIONAL SYMBOL SLASH BAR
<Multi_key> <backslash> <minus>		: "⍀"	U2340 # \ - APL FUNCTIONAL SYMBOL BACKSLASH BAR
<Multi_key> <minus> <backslash>		: "⍀"	U2340 # - \ APL FUNCTIONAL SYMBOL BACKSLASH BAR
<Multi_key> <slash> <U2395>		: "⍁"	U2341 # / ⎕ APL FUNCTIONAL SYMBOL QUAD SLASH
<Multi_key> <U2395> <slash>		: "⍁"	U2341 # ⎕ / APL FUNCTIONAL SYMBOL QUAD SLASH
<Multi_key> <backslash> <U2395>		: "⍂"	U2342 # \ ⎕ APL FUNCTIONAL SYMBOL QUAD BACKSLASH
<Multi_key> <U2395> <backslash>		: "⍂"	U2342 # ⎕ \ APL FUNCTIONAL SYMBOL QUAD BACKSLASH
<Multi_key> <less> <U2395>		: "⍃"	U2343 # < ⎕ APL FUNCTIONAL SYMBOL QUAD LESS-THAN
<Multi_key> <U2395> <less>		: "⍃"	U2343 # ⎕ < APL FUNCTIONAL SYMBOL QUAD LESS-THAN
<Multi_key> <greater> <U2395>		: "⍄"	U2344 # > ⎕ APL FUNCTIONAL SYMBOL QUAD GREATER-THAN
<Multi_key> <U2395> <greater>		: "⍄"	U2344 # ⎕ > APL FUNCTIONAL SYMBOL QUAD GREATER-THAN
<Multi_key> <U2190> <bar>		: "⍅"	U2345 # ← | APL FUNCTIONAL SYMBOL LEFTWARDS VANE
<Multi_key> <bar> <U2190>		: "⍅"	U2345 # | ← APL FUNCTIONAL SYMBOL LEFTWARDS VANE
<Multi_key> <U2192> <bar>		: "⍆"	U2346 # → | APL FUNCTIONAL SYMBOL RIGHTWARDS VANE
<Multi_key> <bar> <U2192>		: "⍆"	U2346 # | → APL FUNCTIONAL SYMBOL RIGHTWARDS VANE
<Multi_key> <U2190> <U2395>		: "⍇"	U2347 # ← ⎕ APL FUNCTIONAL SYMBOL QUAD LEFTWARDS ARROW
<Multi_key> <U2395> <U2190>		: "⍇"	U2347 # ⎕ ← APL FUNCTIONAL SYMBOL QUAD LEFTWARDS ARROW
<Multi_key> <U2192> <U2395>		: "⍈"	U2348 # → ⎕ APL FUNCTIONAL SYMBOL QUAD RIGHTWARDS ARROW
<Multi_key> <U2395> <U2192>		: "⍈"	U2348 # ⎕ → APL FUNCTIONAL SYMBOL QUAD RIGHTWARDS ARROW
<Multi_key> <U25cb> <backslash>		: "⍉"	U2349 # ○ \ APL FUNCTIONAL SYMBOL CIRCLE SLOPE
<Multi_key> <backslash> <U25cb>		: "⍉"	U2349 # \ ○ APL FUNCTIONAL SYMBOL CIRCLE SLOPE
<Multi_key> <underscore> <U22a5>	: "⍊"	U234a # _ ⊥ APL FUNCTIONAL SYMBOL DOWN TACK UNDERBAR
<Multi_key> <U22a5> <underscore>	: "⍊"	U234a # ⊥ _ APL FUNCTIONAL SYMBOL DOWN TACK UNDERBAR
<Multi_key> <U2206> <bar>		: "⍋"	U234b # ∆ | APL FUNCTIONAL SYMBOL DELTA STILE
<Multi_key> <bar> <U2206>		: "⍋"	U234b # | ∆ APL FUNCTIONAL SYMBOL DELTA STILE
<Multi_key> <U2228> <U2395>		: "⍌"	U234c # ∨ ⎕ APL FUNCTIONAL SYMBOL QUAD DOWN CARET
<Multi_key> <U2395> <U2228>		: "⍌"	U234c # ⎕ ∨ APL FUNCTIONAL SYMBOL QUAD DOWN CARET
<Multi_key> <U2206> <U2395>		: "⍍"	U234d # ∆ ⎕ APL FUNCTIONAL SYMBOL QUAD DELTA
<Multi_key> <U2395> <U2206>		: "⍍"	U234d # ⎕ ∆ APL FUNCTIONAL SYMBOL QUAD DELTA
<Multi_key> <U2218> <U22a5>		: "⍎"	U234e # ∘ ⊥ APL FUNCTIONAL SYMBOL DOWN TACK JOT
<Multi_key> <U22a5> <U2218>		: "⍎"	U234e # ⊥ ∘ APL FUNCTIONAL SYMBOL DOWN TACK JOT
<Multi_key> <U2191> <minus>		: "⍏"	U234f # ↑ - APL FUNCTIONAL SYMBOL UPWARDS VANE
<Multi_key> <minus> <U2191>		: "⍏"	U234f # - ↑ APL FUNCTIONAL SYMBOL UPWARDS VANE
<Multi_key> <U2191> <U2395>		: "⍐"	U2350 # ↑ ⎕ APL FUNCTIONAL SYMBOL QUAD UPWARDS ARROW
<Multi_key> <U2395> <U2191>		: "⍐"	U2350 # ⎕ ↑ APL FUNCTIONAL SYMBOL QUAD UPWARDS ARROW
<Multi_key> <macron> <U22a4>		: "⍑"	U2351 # ¯ ⊤ APL FUNCTIONAL SYMBOL UP TACK OVERBAR
<Multi_key> <U22a4> <macron>		: "⍑"	U2351 # ⊤ ¯ APL FUNCTIONAL SYMBOL UP TACK OVERBAR
<Multi_key> <U2207> <bar>		: "⍒"	U2352 # ∇ | APL FUNCTIONAL SYMBOL DEL STILE
<Multi_key> <bar> <U2207>		: "⍒"	U2352 # | ∇ APL FUNCTIONAL SYMBOL DEL STILE
<Multi_key> <U2227> <U2395>		: "⍓"	U2353 # ∧ ⎕ APL FUNCTIONAL SYMBOL QUAD UP CARET
<Multi_key> <U2395> <U2227>		: "⍓"	U2353 # ⎕ ∧ APL FUNCTIONAL SYMBOL QUAD UP CARET
<Multi_key> <U2207> <U2395>		: "⍔"	U2354 # ∇ ⎕ APL FUNCTIONAL SYMBOL QUAD DEL
<Multi_key> <U2395> <U2207>		: "⍔"	U2354 # ⎕ ∇ APL FUNCTIONAL SYMBOL QUAD DEL
<Multi_key> <U2218> <U22a4>		: "⍕"	U2355 # ∘ ⊤ APL FUNCTIONAL SYMBOL UP TACK JOT
<Multi_key> <U22a4> <U2218>		: "⍕"	U2355 # ⊤ ∘ APL FUNCTIONAL SYMBOL UP TACK JOT
<Multi_key> <U2193> <minus>		: "⍖"	U2356 # ↓ - APL FUNCTIONAL SYMBOL DOWNWARDS VANE
<Multi_key> <minus> <U2193>		: "⍖"	U2356 # - ↓ APL FUNCTIONAL SYMBOL DOWNWARDS VANE
<Multi_key> <U2193> <U2395>		: "⍗"	U2357 # ↓ ⎕ APL FUNCTIONAL SYMBOL QUAD DOWNWARDS ARROW
<Multi_key> <U2395> <U2193>		: "⍗"	U2357 # ⎕ ↓ APL FUNCTIONAL SYMBOL QUAD DOWNWARDS ARROW
<Multi_key> <underscore> <apostrophe>	: "⍘"	U2358 # _ ' APL FUNCTIONAL SYMBOL QUOTE UNDERBAR
<Multi_key> <U2206> <underscore>	: "⍙"	U2359 # ∆ _ APL FUNCTIONAL SYMBOL DELTA UNDERBAR
<Multi_key> <underscore> <U2206>	: "⍙"	U2359 # _ ∆ APL FUNCTIONAL SYMBOL DELTA UNDERBAR
<Multi_key> <U22c4> <underscore>	: "⍚"	U235a # ⋄ _ APL FUNCTIONAL SYMBOL DIAMOND UNDERBAR
<Multi_key> <underscore> <U22c4>	: "⍚"	U235a # _ ⋄ APL FUNCTIONAL SYMBOL DIAMOND UNDERBAR
<Multi_key> <U2218> <underscore>	: "⍛"	U235b # ∘ _ APL FUNCTIONAL SYMBOL JOT UNDERBAR
<Multi_key> <underscore> <U2218>	: "⍛"	U235b # _ ∘ APL FUNCTIONAL SYMBOL JOT UNDERBAR
<Multi_key> <U25cb> <underscore>	: "⍜"	U235c # ○ _ APL FUNCTIONAL SYMBOL CIRCLE UNDERBAR
<Multi_key> <underscore> <U25cb>	: "⍜"	U235c # _ ○ APL FUNCTIONAL SYMBOL CIRCLE UNDERBAR
<Multi_key> <U2218> <U2229>		: "⍝"	U235d # ∘ ∩ APL FUNCTIONAL SYMBOL UP SHOE JOT
<Multi_key> <U2229> <U2218>		: "⍝"	U235d # ∩ ∘ APL FUNCTIONAL SYMBOL UP SHOE JOT
<Multi_key> <U2395> <apostrophe>	: "⍞"	U235e # * ¨ APL FUNCTIONAL SYMBOL QUOTE QUAD
<Multi_key> <apostrophe> <U2395>	: "⍞"	U235e # ¨ * APL FUNCTIONAL SYMBOL QUOTE QUAD
<Multi_key> <U25cb> <asterisk>		: "⍟"	U235f # ○ * APL FUNCTIONAL SYMBOL CIRCLE STAR
<Multi_key> <asterisk> <U25cb>		: "⍟"	U235f # * ○ APL FUNCTIONAL SYMBOL CIRCLE STAR
<Multi_key> <colon> <U2395>		: "⍠"	U2360 # : ⎕ APL FUNCTIONAL SYMBOL QUAD COLON
<Multi_key> <U2395> <colon>		: "⍠"	U2360 # ⎕ : APL FUNCTIONAL SYMBOL QUAD COLON
<Multi_key> <diaeresis> <U22a4>		: "⍡"	U2361 # ¨ ⊤ APL FUNCTIONAL SYMBOL UP TACK DIAERESIS
<Multi_key> <U22a4> <diaeresis>		: "⍡"	U2361 # ⊤ ¨ APL FUNCTIONAL SYMBOL UP TACK DIAERESIS
<Multi_key> <diaeresis> <U2207>		: "⍢"	U2362 # ¨ ∇ APL FUNCTIONAL SYMBOL DEL DIAERESIS
<Multi_key> <U2207> <diaeresis>		: "⍢"	U2362 # ∇ ¨ APL FUNCTIONAL SYMBOL DEL DIAERESIS
<Multi_key> <asterisk> <diaeresis>	: "⍣"	U2363 # * ¨ APL FUNCTIONAL SYMBOL STAR DIAERESIS
<Multi_key> <diaeresis> <asterisk>	: "⍣"	U2363 # ¨ * APL FUNCTIONAL SYMBOL STAR DIAERESIS
<Multi_key> <U2218> <diaeresis>		: "⍤"	U2364 # ∘ ¨ APL FUNCTIONAL SYMBOL JOT DIAERESIS
<Multi_key> <diaeresis> <U2218>		: "⍤"	U2364 # ¨ ∘ APL FUNCTIONAL SYMBOL JOT DIAERESIS
<Multi_key> <U25cb> <diaeresis>		: "⍥"	U2365 # ○ ¨ APL FUNCTIONAL SYMBOL CIRCLE DIAERESIS
<Multi_key> <diaeresis> <U25cb>		: "⍥"	U2365 # ¨ ○ APL FUNCTIONAL SYMBOL CIRCLE DIAERESIS
<Multi_key> <U222a> <bar>		: "⍦"	U2366 # ∪ | APL FUNCTIONAL SYMBOL DOWN SHOE STILE
<Multi_key> <bar> <U222a>		: "⍦"	U2366 # | ∪ APL FUNCTIONAL SYMBOL DOWN SHOE STILE
<Multi_key> <U2282> <bar>		: "⍧"	U2367 # ⊂ | APL FUNCTIONAL SYMBOL LEFT SHOE STILE
<Multi_key> <bar> <U2282>		: "⍧"	U2367 # | ⊂ APL FUNCTIONAL SYMBOL LEFT SHOE STILE
<Multi_key> <asciitilde> <diaeresis>	: "⍨"	U2368 # ~ ¨ APL FUNCTIONAL SYMBOL TILDE DIAERESIS
<Multi_key> <diaeresis> <greater>	: "⍩"	U2369 # ¨ > APL FUNCTIONAL SYMBOL GREATER-THAN DIAERESIS
<Multi_key> <greater> <diaeresis>	: "⍩"	U2369 # > ¨ APL FUNCTIONAL SYMBOL GREATER-THAN DIAERESIS
<Multi_key> <U2207> <asciitilde>	: "⍫"	U236b # ∇ ~ APL FUNCTIONAL SYMBOL DEL TILDE
<Multi_key> <asciitilde> <U2207>	: "⍫"	U236b # ~ ∇ APL FUNCTIONAL SYMBOL DEL TILDE
<Multi_key> <0> <asciitilde>		: "⍬"	U236c # 0 ~ APL FUNCTIONAL SYMBOL ZILDE
<Multi_key> <asciitilde> <0>		: "⍬"	U236c # ~ 0 APL FUNCTIONAL SYMBOL ZILDE
<Multi_key> <bar> <asciitilde>		: "⍭"	U236d # | ~ APL FUNCTIONAL SYMBOL STILE TILDE
<Multi_key> <asciitilde> <bar>		: "⍭"	U236d # ~ | APL FUNCTIONAL SYMBOL STILE TILDE
<Multi_key> <semicolon> <underscore>	: "⍮"	U236e # ; _ APL FUNCTIONAL SYMBOL SEMICOLON UNDERBAR
<Multi_key> <U2260> <U2395>		: "⍯"	U236f # ≠ ⎕ APL FUNCTIONAL SYMBOL QUAD NOT EQUAL
<Multi_key> <U2395> <U2260>		: "⍯"	U236f # ⎕ ≠ APL FUNCTIONAL SYMBOL QUAD NOT EQUAL
<Multi_key> <question> <U2395>		: "⍰"	U2370 # ? ⎕ APL FUNCTIONAL SYMBOL QUAD QUESTION
<Multi_key> <U2395> <question>		: "⍰"	U2370 # ⎕ ? APL FUNCTIONAL SYMBOL QUAD QUESTION
<Multi_key> <U2228> <asciitilde>	: "⍱"	U2371 # ∨ ~ APL FUNCTIONAL SYMBOL DOWN CARET TILDE
<Multi_key> <asciitilde> <U2228>	: "⍱"	U2371 # ~ ∨ APL FUNCTIONAL SYMBOL DOWN CARET TILDE
<Multi_key> <U2227> <asciitilde>	: "⍲"	U2372 # ∧ ~ APL FUNCTIONAL SYMBOL UP CARET TILDE
<Multi_key> <asciitilde> <U2227>	: "⍲"	U2372 # ~ ∧ APL FUNCTIONAL SYMBOL UP CARET TILDE
<Multi_key> <U237a> <underscore>	: "⍶"	U2376 # ⍺ _ APL FUNCTIONAL SYMBOL ALPHA UNDERBAR
<Multi_key> <underscore> <U237a>	: "⍶"	U2376 # _ ⍺ APL FUNCTIONAL SYMBOL ALPHA UNDERBAR
<Multi_key> <U220a> <underscore>	: "⍷"	U2377 # ∊ _ APL FUNCTIONAL SYMBOL EPSILON UNDERBAR
<Multi_key> <underscore> <U220a>	: "⍷"	U2377 # _ ∊ APL FUNCTIONAL SYMBOL EPSILON UNDERBAR
<Multi_key> <U2373> <underscore>	: "⍸"	U2378 # ⍳ _ APL FUNCTIONAL SYMBOL IOTA UNDERBAR
<Multi_key> <underscore> <U2373>	: "⍸"	U2378 # _ ⍳ APL FUNCTIONAL SYMBOL IOTA UNDERBAR
<Multi_key> <U2375> <underscore>	: "⍹"	U2379 # ⍵ _ APL FUNCTIONAL SYMBOL OMEGA UNDERBAR
<Multi_key> <underscore> <U2375>	: "⍹"	U2379 # _ ⍵ APL FUNCTIONAL SYMBOL OMEGA UNDERBAR
# Diacritics used in African languages
<dead_acute> <U025B>			: "ɛ́" # LATIN SMALL LETTER EPSILON plus COMBINING ACUTE
<dead_grave> <U025B>			: "ɛ̀" # LATIN SMALL LETTER EPSILON plus COMBINING GRAVE
<dead_circumflex> <U025B>		: "ɛ̂" # LATIN SMALL LETTER EPSILON plus COMBINING CIRCUMFLEX
<dead_caron> <U025B>			: "ɛ̌" # LATIN SMALL LETTER EPSILON plus COMBINING CARON
<dead_macron> <U025B>			: "ɛ̄" # LATIN SMALL LETTER EPSILON plus COMBINING MACRON
<dead_tilde> <U025B>			: "ɛ̃" # LATIN SMALL LETTER EPSILON plus COMBINING TILDE
<dead_acute> <dead_tilde> <U025B>	: "ɛ̃́" # LATIN SMALL LETTER EPSILON plus COMBINING TILDE and COMBINING ACUTE
<dead_grave> <dead_tilde> <U025B>	: "ɛ̃̀" # LATIN SMALL LETTER EPSILON plus COMBINING TILDE and COMBINING GRAVE
<dead_acute> <U0190>			: "Ɛ́" # LATIN CAPITAL LETTER EPSILON plus COMBINING ACUTE
<dead_grave> <U0190>			: "Ɛ̀" # LATIN CAPITAL LETTER EPSILON plus COMBINING GRAVE
<dead_circumflex> <U0190>		: "Ɛ̂" # LATIN CAPITAL LETTER EPSILON plus COMBINING CIRCUMFLEX
<dead_caron> <U0190>			: "Ɛ̌" # LATIN CAPITAL LETTER EPSILON plus COMBINING CARON
<dead_macron> <U0190>			: "Ɛ̄" # LATIN CAPITAL LETTER EPSILON plus COMBINING MACRON
<dead_tilde> <U0190>			: "Ɛ̃" # LATIN CAPITAL LETTER EPSILON plus COMBINING TILDE
<dead_acute> <dead_tilde> <U0190>	: "Ɛ̃́" # LATIN CAPITAL LETTER EPSILON plus COMBINING TILDE and COMBINING ACUTE
<dead_grave> <dead_tilde> <U0190>	: "Ɛ̃̀" # LATIN CAPITAL LETTER EPSILON plus COMBINING TILDE and COMBINING GRAVE
<dead_acute> <U0269>			: "ɩ́" # LATIN SMALL LETTER IOTA plus COMBINING ACUTE
<dead_grave> <U0269>			: "ɩ̀" # LATIN SMALL LETTER IOTA plus COMBINING GRAVE
<dead_circumflex> <U0269>		: "ɩ̂" # LATIN SMALL LETTER IOTA plus COMBINING CIRCUMFLEX
<dead_caron> <U0269>			: "ɩ̌" # LATIN SMALL LETTER IOTA plus COMBINING CARON
<dead_macron> <U0269>			: "ɩ̄" # LATIN SMALL LETTER IOTA plus COMBINING MACRON
<dead_acute> <U0196>			: "Ɩ́" # LATIN CAPITAL LETTER IOTA plus COMBINING ACUTE
<dead_grave> <U0196>			: "Ɩ̀" # LATIN CAPITAL LETTER IOTA plus COMBINING GRAVE
<dead_circumflex> <U0196>		: "Ɩ̂" # LATIN CAPITAL LETTER IOTA plus COMBINING CIRCUMFLEX
<dead_caron> <U0196>			: "Ɩ̌" # LATIN CAPITAL LETTER IOTA plus COMBINING CARON
<dead_macron> <U0196>			: "Ɩ̄" # LATIN CAPITAL LETTER IOTA plus COMBINING MACRON
<dead_acute> <U0254>			: "ɔ́" # LATIN SMALL LETTER OPEN O plus COMBINING ACUTE
<dead_grave> <U0254>			: "ɔ̀" # LATIN SMALL LETTER OPEN O plus COMBINING GRAVE
<dead_circumflex> <U0254>		: "ɔ̂" # LATIN SMALL LETTER OPEN O plus COMBINING CIRCUMFLEX
<dead_caron> <U0254>			: "ɔ̌" # LATIN SMALL LETTER OPEN O plus COMBINING CARON
<dead_macron> <U0254>			: "ɔ̄" # LATIN SMALL LETTER OPEN O plus COMBINING MACRON
<dead_tilde> <U0254>			: "ɔ̃" # LATIN SMALL LETTER OPEN O plus COMBINING TILDE
<dead_acute> <dead_tilde> <U0254>	: "ɔ̃́" # LATIN SMALL LETTER OPEN O plus COMBINING TILDE and COMBINING ACUTE
<dead_grave> <dead_tilde> <U0254>	: "ɔ̃̀" # LATIN SMALL LETTER OPEN O plus COMBINING TILDE and COMBINING GRAVE
<dead_acute> <U0186>			: "Ɔ́" # LATIN CAPITAL LETTER OPEN O plus COMBINING ACUTE
<dead_grave> <U0186>			: "Ɔ̀" # LATIN CAPITAL LETTER OPEN O plus COMBINING GRAVE
<dead_circumflex> <U0186>		: "Ɔ̂" # LATIN CAPITAL LETTER OPEN O plus COMBINING CIRCUMFLEX
<dead_caron> <U0186>			: "Ɔ̌" # LATIN CAPITAL LETTER OPEN O plus COMBINING CARON
<dead_macron> <U0186>			: "Ɔ̄" # LATIN CAPITAL LETTER OPEN O plus COMBINING MACRON
<dead_tilde> <U0186>			: "Ɔ̃" # LATIN CAPITAL LETTER OPEN O plus COMBINING TILDE
<dead_acute> <dead_tilde> <U0186>	: "Ɔ̃́" # LATIN CAPITAL LETTER OPEN O plus COMBINING TILDE and COMBINING ACUTE
<dead_grave> <dead_tilde> <U0186>	: "Ɔ̃̀" # LATIN CAPITAL LETTER OPEN O plus COMBINING TILDE and COMBINING GRAVE
<dead_acute> <U01DD>			: "ǝ́" # LATIN SMALL LETTER TURNED E plus COMBINING ACUTE
<dead_grave> <U01DD>			: "ǝ̀" # LATIN SMALL LETTER TURNED E plus COMBINING GRAVE
<dead_circumflex> <U01DD>		: "ǝ̂" # LATIN SMALL LETTER TURNED E plus COMBINING CIRCUMFLEX
<dead_caron> <U01DD>			: "ǝ̌" # LATIN SMALL LETTER TURNED E plus COMBINING CARON
<dead_macron> <U01DD>			: "ǝ̄" # LATIN SMALL LETTER TURNED E plus COMBINING MACRON
<dead_tilde> <U01DD>			: "ǝ̃" # LATIN SMALL LETTER TURNED E plus COMBINING TILDE
<dead_acute> <dead_tilde> <U01DD>	: "ǝ̃́" # LATIN SMALL LETTER TURNED E plus COMBINING TILDE and COMBINING ACUTE
<dead_grave> <dead_tilde> <U01DD>	: "ǝ̃̀" # LATIN SMALL LETTER TURNED E plus COMBINING TILDE and COMBINING GRAVE
<dead_acute> <U018E>			: "Ǝ́" # LATIN CAPITAL LETTER TURNED E plus COMBINING ACUTE
<dead_grave> <U018E>			: "Ǝ̀" # LATIN CAPITAL LETTER TURNED E plus COMBINING GRAVE
<dead_circumflex> <U018E>		: "Ǝ̂" # LATIN CAPITAL LETTER TURNED E plus COMBINING CIRCUMFLEX
<dead_caron> <U018E>			: "Ǝ̌" # LATIN CAPITAL LETTER TURNED E plus COMBINING CARON
<dead_macron> <U018E>			: "Ǝ̄" # LATIN CAPITAL LETTER TURNED E plus COMBINING MACRON
<dead_tilde> <U018E>			: "Ǝ̃" # LATIN CAPITAL LETTER TURNED E plus COMBINING TILDE
<dead_acute> <dead_tilde> <U018E>	: "Ǝ̃́" # LATIN CAPITAL LETTER TURNED E plus COMBINING TILDE and COMBINING ACUTE
<dead_grave> <dead_tilde> <U018E>	: "Ǝ̃̀" # LATIN CAPITAL LETTER TURNED E plus COMBINING TILDE and COMBINING GRAVE
<dead_acute> <U028B>			: "ʋ́" # LATIN SMALL LETTER V WITH HOOK plus COMBINING ACUTE
<dead_grave> <U028B>			: "ʋ̀" # LATIN SMALL LETTER V WITH HOOK plus COMBINING GRAVE
<dead_circumflex> <U028B>		: "ʋ̂" # LATIN SMALL LETTER V WITH HOOK plus COMBINING CIRCUMFLEX
<dead_caron> <U028B>			: "ʋ̌" # LATIN SMALL LETTER V WITH HOOK plus COMBINING CARON
<dead_macron> <U028B>			: "ʋ̄" # LATIN SMALL LETTER V WITH HOOK plus COMBINING MACRON
<dead_acute> <U01B2>			: "Ʋ́" # LATIN CAPITAL LETTER V WITH HOOK plus COMBINING ACUTE
<dead_grave> <U01B2>			: "Ʋ̀" # LATIN CAPITAL LETTER V WITH HOOK plus COMBINING GRAVE
<dead_circumflex> <U01B2>		: "Ʋ̂" # LATIN CAPITAL LETTER V WITH HOOK plus COMBINING CIRCUMFLEX
<dead_caron> <U01B2>			: "Ʋ̌" # LATIN CAPITAL LETTER V WITH HOOK plus COMBINING CARON
<dead_macron> <U01B2>			: "Ʋ̄" # LATIN CAPITAL LETTER V WITH HOOK plus COMBINING MACRON
<dead_acute> <U028A>			: "ʊ́" # LATIN SMALL LETTER UPSILON plus COMBINING ACUTE
<dead_grave> <U028A>			: "ʊ̀" # LATIN SMALL LETTER UPSILONK plus COMBINING GRAVE
<dead_circumflex> <U028A>		: "ʊ̂" # LATIN SMALL LETTER UPSILON plus COMBINING CIRCUMFLEX
<dead_caron> <U028A>			: "ʊ̌" # LATIN SMALL LETTER UPSILON plus COMBINING CARON
<dead_macron> <U028A>			: "ʊ̄" # LATIN SMALL LETTER UPSILON plus COMBINING MACRON
<dead_acute> <U01B1>			: "Ʊ́" # LATIN CAPITAL LETTER UPSILON plus COMBINING ACUTE
<dead_grave> <U01B1>			: "Ʊ̀" # LATIN CAPITAL LETTER UPSILONK plus COMBINING GRAVE
<dead_circumflex> <U01B1>		: "Ʊ̂" # LATIN CAPITAL LETTER UPSILON plus COMBINING CIRCUMFLEX
<dead_caron> <U01B1>			: "Ʊ̌" # LATIN CAPITAL LETTER UPSILON plus COMBINING CARON
<dead_macron> <U01B1>			: "Ʊ̄" # LATIN CAPITAL LETTER UPSILON plus COMBINING MACRON
<dead_acute> <dead_tilde> <a>		: "ã́" # LATIN SMALL LETTER A plus COMBINING TILDE and COMBINING ACUTE
<dead_grave> <dead_tilde> <a>		: "ã̀" # LATIN SMALL LETTER A plus COMBINING TILDE and COMBINING GRAVE
<dead_acute> <dead_tilde> <A>		: "Ã́" # LATIN CAPITAL LETTER A plus COMBINING TILDE and COMBINING ACUTE
<dead_grave> <dead_tilde> <A>		: "Ã̀" # LATIN CAPITAL LETTER A plus COMBINING TILDE and COMBINING GRAVE
<dead_acute> <dead_tilde> <e>		: "ẽ́" # LATIN SMALL LETTER E plus COMBINING TILDE and COMBINING ACUTE
<dead_grave> <dead_tilde> <e>		: "ẽ̀" # LATIN SMALL LETTER E plus COMBINING TILDE and COMBINING GRAVE
<dead_acute> <dead_tilde> <E>		: "Ẽ́" # LATIN CAPITAL LETTER E plus COMBINING TILDE and COMBINING ACUTE
<dead_grave> <dead_tilde> <E>		: "Ẽ̀" # LATIN CAPITAL LETTER E plus COMBINING TILDE and COMBINING GRAVE
<dead_acute> <dead_tilde> <i>		: "ĩ́" # LATIN SMALL LETTER I plus COMBINING TILDE and COMBINING ACUTE
<dead_grave> <dead_tilde> <i>		: "ĩ̀" # LATIN SMALL LETTER I plus COMBINING TILDE and COMBINING GRAVE
<dead_acute> <dead_tilde> <I>		: "Ĩ́" # LATIN CAPITAL LETTER I plus COMBINING TILDE and COMBINING ACUTE
<dead_grave> <dead_tilde> <I>		: "Ĩ̀" # LATIN CAPITAL LETTER I plus COMBINING TILDE and COMBINING GRAVE
<dead_grave> <dead_tilde> <o>		: "õ̀" # LATIN SMALL LETTER O plus COMBINING TILDE and COMBINING GRAVE
<dead_grave> <dead_tilde> <O>		: "Õ̀" # LATIN CAPITAL LETTER O plus COMBINING TILDE and COMBINING GRAVE
<dead_grave> <dead_tilde> <u>		: "ũ̀" # LATIN SMALL LETTER U plus COMBINING TILDE and COMBINING GRAVE
<dead_grave> <dead_tilde> <U>		: "Ũ̀" # LATIN CAPITAL LETTER U plus COMBINING TILDE and COMBINING GRAVE
<dead_grave> <m>			: "m̀" # LATIN SMALL LETTER M plus COMBINING GRAVE
<dead_grave> <M>			: "M̀" # LATIN CAPITAL LETTER M plus COMBINING GRAVE
<dead_acute> <eng>			: "ŋ́" # LATIN SMALL LETTER ENG plus COMBINING ACUTE
<dead_grave> <eng>			: "ŋ̀" # LATIN SMALL LETTER ENG plus COMBINING GRAVE
<dead_acute> <ENG>			: "Ŋ́" # LATIN CAPITAL LETTER ENG plus COMBINING ACUTE
<dead_grave> <ENG>			: "Ŋ̀" # LATIN CAPITAL LETTER ENG plus COMBINING GRAVE
""".encode("utf-8")
