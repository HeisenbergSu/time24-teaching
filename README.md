# 24时计时法教学系统

一个用于小学三年级下册"24时计时法"教学的互动教学系统，采用 Vue2 + Python Flask + SQLite 技术栈。

## 功能模块

### 1. 课前探索
- **旧知复习**：包含一、二年级时间知识的互动练习题
- **情景导入**：展示时间流转（钟表走两圈）的数字动画视频

### 2. 新知学习
- **钟表一天转两圈**：通过地球、太阳、月亮的互动场景，让学生直观感受时针一天转两圈
- **时间与天色**：展示早上8点和晚上8点的对比，让学生理解相同时针位置但天色不同
- **互动时钟**：可手动调节时间，观察时针转动和背景变化

### 3. 生活应用
- **12时计时法与24时计时法转换**：
  - 时间尺展示（化曲为直）
  - 转换规则说明
  - 生活场景练习（火车票时间、咖啡店营业时间等）

### 4. 成就挑战
- **综合测验**：包含新知学习和生活应用的练习题
- **排行榜**：显示全班学生的成绩排名

### 5. 教师后台
- **数据统计**：查看整体数据、模块统计
- **学生成绩**：查看所有学生的成绩列表
- **错题分析**：统计每道题的错误率，定位教学难点

## 技术栈

- **前端**：Vue 2.6.14 + Vue Router + Element UI + Axios
- **后端**：Python Flask + Flask-CORS + SQLAlchemy
- **数据库**：SQLite

## 安装与运行

### 后端设置

1. 进入后端目录：
```bash
cd backend
```

2. 安装Python依赖：
```bash
pip install -r requirements.txt
```

3. 初始化数据库和题目数据：
```bash
python init_data.py
```

4. 启动后端服务：
```bash
python app.py
```

后端服务将在 `http://localhost:5000` 启动

### 前端设置

1. 进入前端目录：
```bash
cd frontend
```

2. 安装依赖：
```bash
npm install
```

3. 启动开发服务器：
```bash
npm run serve
```

前端服务将在 `http://localhost:8080` 启动

### 生产环境构建

构建前端：
```bash
cd frontend
npm run build
```

构建后的文件在 `frontend/dist` 目录，可以部署到静态文件服务器。

### 跨平台打包（Windows / macOS）

系统支持一键打包为可执行文件，适配 Windows 和 macOS 操作系统。

#### Windows 平台打包

1. **使用批处理脚本（推荐）**：
   ```bash
   双击 一键打包.bat
   ```

2. **使用命令行**：
   ```bash
   python build_project.py
   ```

打包完成后，在 `release/Windows` 目录下找到打包好的程序。

#### macOS 平台打包

1. **使用 Shell 脚本（推荐）**：
   ```bash
   chmod +x 一键打包.sh
   ./一键打包.sh
   ```

2. **使用命令行**：
   ```bash
   python3 build_project.py
   ```

打包完成后，在 `release/macOS` 目录下找到打包好的程序。

**注意**：
- 在 Windows 上打包只能生成 Windows 版本
- 在 macOS 上打包只能生成 macOS 版本
- 打包脚本会自动检测操作系统并生成对应平台版本

详细打包说明请查看：[打包部署指南.md](./打包部署指南.md)

## 使用说明

### 学生使用

1. 访问系统首页
2. 输入姓名和班级注册
3. 依次完成以下模块：
   - **课前探索**：复习旧知识，观看时间流转动画
   - **新知学习**：学习24时计时法，理解钟表转两圈
   - **生活应用**：练习12时和24时计时法的转换
   - **成就挑战**：完成综合测验，查看排行榜

### 教师使用

1. 访问 `/teacher` 路由或点击首页的"教师入口"
2. 使用默认账号登录：
   - 用户名：`teacher`
   - 密码：`teacher123`
3. 查看：
   - **数据统计**：整体学习情况
   - **学生成绩**：每个学生的详细成绩
   - **错题分析**：了解哪些题目错误率高，便于针对性教学

## 项目结构

```
time24-teaching/
├── backend/                 # 后端代码
│   ├── app.py              # Flask主应用
│   ├── models.py           # 数据库模型
│   ├── init_data.py        # 初始化题目数据
│   ├── requirements.txt    # Python依赖
│   └── time24_teaching.db  # SQLite数据库（运行后生成）
├── frontend/               # 前端代码
│   ├── src/
│   │   ├── components/     # Vue组件
│   │   │   ├── ExploreModule.vue      # 课前探索模块
│   │   │   ├── LearnModule.vue        # 新知学习模块
│   │   │   ├── PracticeModule.vue     # 生活应用模块
│   │   │   ├── ChallengeModule.vue    # 成就挑战模块
│   │   │   ├── ClockAnimation.vue     # 时钟动画组件
│   │   │   └── TimeScale.vue          # 时间尺组件
│   │   ├── views/          # 页面视图
│   │   │   ├── Home.vue               # 学生首页
│   │   │   └── TeacherDashboard.vue   # 教师后台
│   │   ├── router/         # 路由配置
│   │   ├── App.vue         # 根组件
│   │   └── main.js         # 入口文件
│   ├── package.json        # 前端依赖配置
│   └── vue.config.js       # Vue配置
└── README.md               # 项目说明文档
```

## 数据库设计

- **students**：学生表
- **teachers**：教师表
- **questions**：题目表
- **student_answers**：学生答题记录表

## 特色功能

1. **直观的时钟动画**：通过地球、太阳、月亮的场景，帮助学生理解时间流转
2. **交互式时间尺**：将圆形钟面化曲为直，便于理解12时和24时计时法的对应关系
3. **生活场景应用**：结合火车票、咖啡店等实际场景，增强实用性
4. **数据驱动的教学**：教师可以通过错题分析，精准定位教学难点

## 开发说明

### 添加新题目

修改 `backend/init_data.py` 文件，在对应的题目列表中添加新题目：

```python
{
    'question': '题目内容',
    'options': json.dumps(['选项1', '选项2', '选项3', '选项4']),
    'correct_answer': '正确答案',
    'module_type': 'explore'  # 或 'practice', 'challenge'
}
```

然后重新运行 `python init_data.py`

## 注意事项

- 确保Python版本 >= 3.6
- 确保Node.js版本 >= 12.0
- 首次运行需要先执行 `init_data.py` 初始化数据
- 默认教师账号请在生产环境中修改密码

## 许可证

本项目仅用于教学目的。

## 作者

小学教师 - 24时计时法教学系统

