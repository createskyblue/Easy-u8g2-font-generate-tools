
void Menu_Init(void) {
    file        tmpFile;
    fileData*   tmpFileData = NULL;
    folderLevel* tmpFolderLevel = NULL;
    cVector tmpMenuLevel = NULL;
    jumpData* tmpJumpData = NULL;

    /*////////////////////////////////////////////////创建第0层菜单*/
    //创建第0层文件容器
    cVector MenuLevel_0 = cVector_create(sizeof(file));
    tmpFolderLevel = (folderLevel*)rt_malloc(sizeof(folderLevel));
    
    //创建第0层菜单第0个文件
    tmpFile.name = "1、天线校准";
    tmpFile.icon = NULL;
    tmpFile.type = F_Menu_Op;
    tmpFile.data = AntennaCalibration_GUI;
    //将选项文件扔进第1层文件容器中
    cVector_pushback(MenuLevel_0, &tmpFile);

    //创建第0层菜单第1个文件
    sprintf(str_mainMenuSetTilt,"2、设置倾角");
    tmpFile.name = str_mainMenuSetTilt;        //2、设置倾角(0.0°-6.0°) //动态文本
    tmpFile.icon = NULL;
    tmpFile.type = Num_Bar_Menu_Op;
    tmpFile.data = (void*)&AcqAngle_NumBar;
    //将选项文件扔进文件夹容器中
    cVector_pushback(MenuLevel_0, &tmpFile);

    //创建第0层菜单第2个文件
    tmpFile.name = "3、天线信息";
    tmpFile.icon = NULL;
    tmpFile.type = Jump_Menu_Op;
    //将选项文件扔进文件夹容器中
    cVector_pushback(MenuLevel_0, &tmpFile);

    //创建第0层菜单第3个文件
    tmpFile.name = "4、配置文件";
    tmpFile.icon = NULL;
    tmpFile.type = Jump_Menu_Op;
    //设置跳转结构体
    tmpJumpData                     = (jumpData*)rt_malloc(sizeof(jumpData));
    tmpJumpData->targetFolder       = &ConfigMenuEnterFolder;
    tmpJumpData->targetFileIndex    = 0;
    tmpJumpData->function           = ReadSDConfigFile;
    //文件 绑定 跳转结构体
    tmpFile.data = (void*)tmpJumpData;
    //将选项文件扔进文件夹容器中
    cVector_pushback(MenuLevel_0, &tmpFile);



    //创建第0层菜单第4个文件
    tmpFile.name = "5、固件更新";
    tmpFile.icon = NULL;
    tmpFile.type = Jump_Menu_Op;
    //设置跳转结构体
    tmpJumpData                     = (jumpData*)rt_malloc(sizeof(jumpData));
    tmpJumpData->targetFolder       = &FirmwareMenuEnterFolder;
    tmpJumpData->targetFileIndex    = 0;
    tmpJumpData->function           = ReadSDFirmwareFile;
    //文件 绑定 跳转结构体
    tmpFile.data = (void*)tmpJumpData; 
    //将选项文件扔进文件夹容器中
    cVector_pushback(MenuLevel_0, &tmpFile);


    //创建第0层菜单第5个文件
    tmpFile.name = "6、其他设置";
    tmpFile.icon = NULL;
    tmpFile.type = Jump_Menu_Op;
    //将选项文件扔进文件夹容器中
    cVector_pushback(MenuLevel_0, &tmpFile);

    //设置文件夹结构体
    tmpFolderLevel->folder = MenuLevel_0;
    tmpFolderLevel->firstLineIndex   = 0;
    tmpFolderLevel->backFolder = NULL;  //失能返回功能
    tmpFolderLevel->name = "主菜单";
    tmpFolderLevel->function = AC_InfoProcess;    //进入文件夹时不执行函数
    //设置第0层菜单为主菜单入口
    mainMenuEnterFolder = tmpFolderLevel;

    //初始化跳转结构体：注意：必须先初始化菜单，再初始化天线列表，不然无法跳转成功
    //设置跳转结构体
    jump2MainMenu           = (jumpData*)rt_malloc(sizeof(jumpData));
    jump2MainMenu->targetFolder       = mainMenuEnterFolder;  //跳转目标始终指向主菜单入口,注意必须先初始化主菜单再初始化天线列表
    jump2MainMenu->targetFileIndex    = 0;      //索引指向当前的文件
    jump2MainMenu->function           = NULL;

    /*////////////////////////////////////////////////创建第2层菜单*/
    //创建文件容器
    cVector MenuLevel_2 = cVector_create(sizeof(file));
    tmpFolderLevel = (folderLevel*)rt_malloc(sizeof(folderLevel));

    //创建第1个文件
    tmpFile.name = "1、输出电压";
    tmpFile.icon = NULL;
    tmpFile.type = Jump_Menu_Op;
    //将选项文件扔进文件容器中
    cVector_pushback(MenuLevel_2, &tmpFile);
    //设置跳转结构体
    tmpJumpData                     = (jumpData*)rt_malloc(sizeof(jumpData));
    tmpJumpData->targetFolder       = tmpFolderLevel;
    tmpJumpData->targetFileIndex    = cVector_length(MenuLevel_2) - 1;      //索引指向当前的文件
    tmpJumpData->function           = NULL;
    //文件 绑定 跳转结构体
    ((file*)cVector_at(MenuLevel_0,5))->data = (void*)tmpJumpData;

    //创建第2个文件
    tmpFile.name = "2、语言";
    tmpFile.icon = NULL;
    tmpFile.type = Jump_Menu_Op;
    //将选项文件扔进文件夹容器中
    cVector_pushback(MenuLevel_2, &tmpFile);

    //创建第3个文件
    tmpFile.name = "3、关于";
    tmpFile.icon = NULL;
    tmpFile.type = Menu_NULL_OP;
    //将选项文件扔进文件夹容器中
    cVector_pushback(MenuLevel_2, &tmpFile);

    //设置文件夹结构体
    tmpFolderLevel->folder  = MenuLevel_2;
    tmpFolderLevel->firstLineIndex   = 0;
    tmpFolderLevel->name = "其他设置";
    tmpFolderLevel->function = NULL;    //进入文件夹时不执行函数

    /*////////////////////////////////////////////////创建 语言设置 菜单*/
    //创建文件容器
    cVector MenuLevel_lang = cVector_create(sizeof(file));
    tmpFolderLevel = (folderLevel*)rt_malloc(sizeof(folderLevel));

    //创建第0个文件
    tmpFile.name = "1.Chinese";
    tmpFile.icon = NULL;
    tmpFile.type = RadioBox_Menu_OP;
    tmpFile.data = &lang;       //绑定单选框内容
    //将选项文件扔进文件容器中
    cVector_pushback(MenuLevel_lang, &tmpFile);
    //设置跳转结构体
    tmpJumpData                     = (jumpData*)rt_malloc(sizeof(jumpData));
    tmpJumpData->targetFolder       = tmpFolderLevel;
    tmpJumpData->targetFileIndex    = cVector_length(MenuLevel_lang) - 1;      //索引指向当前的文件
    tmpJumpData->function           = NULL;
    //文件 绑定 跳转结构体
    ((file*)cVector_at(MenuLevel_2,1))->data = (void*)tmpJumpData;

    //创建第1个文件
    tmpFile.name = "2.English";
    tmpFile.icon = NULL;
    tmpFile.type = RadioBox_Menu_OP;
    tmpFile.data = &lang;       //绑定单选框内容
    //将选项文件扔进文件夹容器中
    cVector_pushback(MenuLevel_lang, &tmpFile);

    //设置文件夹结构体
    tmpFolderLevel->folder  = MenuLevel_lang;
    tmpFolderLevel->firstLineIndex   = 0;
    tmpFolderLevel->name = "Language";
    tmpFolderLevel->function = NULL;    //进入文件夹时不执行函数
  

    /*////////////////////////////////////////////////创建第3层菜单*/
    //创建文件容器
    cVector MenuLevel_3 = cVector_create(sizeof(file));
    tmpFolderLevel = (folderLevel*)rt_malloc(sizeof(folderLevel));

    //创建第0个文件
    tmpFile.name = "1、天线型号";
    tmpFile.icon = NULL;
    tmpFile.type = Text_Menu_Op;
    tmpFile.data = &Menu_ACInfo_Model;
    //将选项文件扔进文件容器中
    cVector_pushback(MenuLevel_3, &tmpFile);
    //设置跳转结构体
    tmpJumpData                     = (jumpData*)rt_malloc(sizeof(jumpData));
    tmpJumpData->targetFolder       = tmpFolderLevel;
    tmpJumpData->targetFileIndex    = cVector_length(MenuLevel_3) - 1;      //索引指向当前的文件
    tmpJumpData->function           = NULL;                       //跳转后执行函数
    //文件 绑定 跳转结构体
    ((file*)cVector_at(MenuLevel_0,2))->data = (void*)tmpJumpData;

    //创建第1个文件
    tmpFile.name = "2、频段";
    tmpFile.icon = NULL;
    tmpFile.type = Text_Menu_Op;
    tmpFile.data = &Menu_ACInfo_Freq;
    //将选项文件扔进文件夹容器中
    cVector_pushback(MenuLevel_3, &tmpFile);

    //创建第2个文件
    tmpFile.name = "3、增益";
    tmpFile.icon = NULL;
    tmpFile.type = Text_Menu_Op;
    tmpFile.data = &Menu_ACInfo_Gain;
    //将选项文件扔进文件夹容器中
    cVector_pushback(MenuLevel_3, &tmpFile);

    //创建第3个文件
    tmpFile.name = "4、波瓣宽度";
    tmpFile.icon = NULL;
    tmpFile.type = Text_Menu_Op;
    tmpFile.data = &Menu_ACInfo_Beamwidth;
    //将选项文件扔进文件夹容器中
    cVector_pushback(MenuLevel_3, &tmpFile);

    //创建第4个文件
    tmpFile.name = "5、最小倾角";
    tmpFile.icon = NULL;
    tmpFile.type = Text_Menu_Op;
    tmpFile.data = &Menu_ACInfo_MinTilt;
    //将选项文件扔进文件夹容器中
    cVector_pushback(MenuLevel_3, &tmpFile);

    //创建第5个文件
    tmpFile.name = "6、最大倾角";
    tmpFile.icon = NULL;
    tmpFile.type = Text_Menu_Op;
    tmpFile.data = &Menu_ACInfo_MaxTilt;
    //将选项文件扔进文件夹容器中
    cVector_pushback(MenuLevel_3, &tmpFile);

    //创建第6个文件
    tmpFile.name = "7、硬件版本";
    tmpFile.icon = NULL;
    tmpFile.type = Text_Menu_Op;
    tmpFile.data = &Menu_ACInfo_HW_Ver;
    //将选项文件扔进文件夹容器中
    cVector_pushback(MenuLevel_3, &tmpFile);

    //创建第7个文件
    tmpFile.name = "8、固件版本";
    tmpFile.icon = NULL;
    tmpFile.type = Text_Menu_Op;
    tmpFile.data = &Menu_ACInfo_FW_Ver;
    //将选项文件扔进文件夹容器中
    cVector_pushback(MenuLevel_3, &tmpFile);

    //创建第8个文件
    tmpFile.name = "9、序列号";
    tmpFile.icon = NULL;
    tmpFile.type = Text_Menu_Op;
    tmpFile.data = &Menu_ACInfo_UUID;
    //将选项文件扔进文件夹容器中
    cVector_pushback(MenuLevel_3, &tmpFile);

    //设置文件夹结构体
    tmpFolderLevel->folder = MenuLevel_3;
    tmpFolderLevel->firstLineIndex   = 0;
    tmpFolderLevel->name = "天线信息";
    tmpFolderLevel->function = NULL;    //进入文件夹时不执行函数

    /*////////////////////////////////////////////////创建 输出电压 菜单*/
    //创建文件容器
    cVector MenuLevel_OutputVol = cVector_create(sizeof(file));
    tmpFolderLevel = (folderLevel*)rt_malloc(sizeof(folderLevel));

    //创建第0个文件
    tmpFile.name = "1、电池电压输出";
    tmpFile.icon = NULL;
    tmpFile.type = RadioBox_Menu_OP;
    tmpFile.data = &Sys_OutputVol;       //绑定单选框内容
    //将选项文件扔进文件容器中
    cVector_pushback(MenuLevel_OutputVol, &tmpFile);
    //设置跳转结构体
    tmpJumpData                     = (jumpData*)rt_malloc(sizeof(jumpData));
    tmpJumpData->targetFolder       = tmpFolderLevel;
    tmpJumpData->targetFileIndex    = cVector_length(MenuLevel_OutputVol) - 1;      //索引指向当前的文件
    tmpJumpData->function           = NULL;
    //文件 绑定 跳转结构体
    ((file*)cVector_at(MenuLevel_2,0))->data = (void*)tmpJumpData;

    //创建第1个文件
    tmpFile.name = "2、使用24V输出";
    tmpFile.icon = NULL;
    tmpFile.type = RadioBox_Menu_OP;
    tmpFile.data = &Sys_OutputVol;       //绑定单选框内容
    //将选项文件扔进文件夹容器中
    cVector_pushback(MenuLevel_OutputVol, &tmpFile);

    //设置文件夹结构体
    tmpFolderLevel->folder  = MenuLevel_OutputVol;
    tmpFolderLevel->firstLineIndex   = 0;
    tmpFolderLevel->name = "输出电压";
    tmpFolderLevel->function = NULL;    //进入文件夹时不执行函数

    
}
