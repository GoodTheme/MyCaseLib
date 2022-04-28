# MyCaseLib


这是一个诉讼案件管理工具（数据库），用于记录案件的基本信息、待办事项和事件记录，方便随时检索、查看。同时，可以查看当日（及15日内）todo-list，也可按既定套路快速生成并复制一些信息。
软件里预设了一些模板，包括民事诉讼和仲裁两种案件类型，以及相应的当事人和联系人类型，可以通过自定义添加或修改这些模板。
因此，除了诉讼案件以外，也许也可以用于管理其他事务。



mac版软件为状态栏app，默认不在dock显示，但与此同时也不显示菜单栏。
如果需要显示菜单栏和dock图标，可以查看包内容，修改Contents文件下的Info.plist中“<key>LSUIElement</key>”下一行为“<false/>”。未来版本争取实现仅在显示主界面时显示dock和菜单栏。
windows版本无状态栏部分。



因为是自用为主，因此大部分功能基于个人习惯设计，加上mac版无正常菜单栏（有也不好用，距离太远），因此许多交互都是是通过右键实现，建议多尝试。
