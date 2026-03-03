# Bilibili AI Video - Task Board

## Project Phases

### M1: Data Collection (Completed ✓)
- [x] M1.1: Project initialization
- [x] M1.2: Bilibili collector implementation
- [x] M1.3: Heat calculator

### M2: Prompt Generation (Completed ✓)
- [x] M2.1: LLM API integration
  - [x] DeepSeek client
  - [x] Anthropic client (backup)
  - [x] Configuration management
- [x] M2.2: Prompt generation service
  - [x] PromptGenerator class
  - [x] Three template types (HOT_INTERPRET, KNOWLEDGE, ROUNDUP)
- [x] M2.3: Prompt template design
  - [x] Title suggestions (3)
  - [x] Core viewpoints (3-5)
  - [x] Video structure (opening, body, ending)
  - [x] Ending interaction
  - [x] Estimated duration
- [x] M2.4: Quality evaluation
  - [x] Basic quality scoring logic
  - [x] Prompt completeness check

### M3: Video Generation (Completed ✓)
- [x] M3.1: Video generation API clients
  - [x] VeADK client (primary)
  - [x] Pika client (backup)
  - [x] Runway client (backup)
- [x] M3.2: Video generation service
  - [x] VideoGenerator class
  - [x] Async generation support
  - [x] Provider fallback logic
- [x] M3.3: Cover image generation
  - [x] CoverGenerator class
  - [x] Multiple styles (BOLD, MINIMAL, COLORFUL, TEXT_HEAVY)
  - [x] Placeholder generation (PIL-based)
- [x] M3.4: Unit tests
  - [x] 22 tests passing
  - [x] Coverage: models, clients, generator, cover

### M4: Publishing (Completed ✓)
- [x] M4.1: Bilibili OAuth authentication
  - [x] OAuth 2.0 implementation (src/publisher/oauth.py)
  - [x] Token storage and refresh mechanism
  - [x] Configuration: APP_KEY, APP_SECRET, REDIRECT_URI
  - [x] Mock mode for testing
- [x] M4.2: Bilibili publish service
  - [x] BilibiliPublisher class (src/publisher/bilibili.py)
  - [x] Video upload interface
  - [x] Metadata: title, description, tags, category
  - [x] Scheduled publishing support
- [x] M4.3: Publish record management
  - [x] SQLite database (src/publisher/database.py)
  - [x] Record video info, status, timestamps
  - [x] Query publish history
- [x] M4.4: Unit tests
  - [x] 22 tests passing
  - [x] Coverage: oauth, database, publisher, scheduler

---

## Development Log

### 2026-03-02

**M2 Development - Prompt Generation Service**

Implemented the following modules:

1. **LLM Client** (`src/prompt/client.py`)
   - DeepSeekClient: Primary LLM provider
   - AnthropicClient: Backup provider
   - Unified interface via LLMClient abstract class

2. **Configuration** (`src/prompt/config.py`)
   - LLMConfig with environment variable support
   - Supported vars: LLM_PROVIDER, DEEPSEEK_API_KEY, ANTHROPIC_API_KEY, etc.

3. **Data Models** (`src/prompt/models.py`)
   - TemplateType enum (HOT_INTERPRET, KNOWLEDGE, ROUNDUP)
   - GeneratedPrompt with all required fields

4. **Templates** (`src/prompt/templates.py`)
   - Three template types with Chinese prompts
   - Format template with topic data

5. **Generator** (`src/prompt/generator.py`)
   - PromptGenerator class
   - Auto-selection of template type based on weights (60/25/15)
   - Quality scoring (0-1)
   - JSON parsing from LLM response

6. **Tests** (`tests/test_prompt.py`)
   - 12 unit tests passing
   - Coverage: config, templates, generation, validation

**Next Steps:**
- Run actual LLM API test with real API keys
- Consider adding more template variations
- Implement retry logic for API failures

---

### 2026-03-02 (continued)

**M3 Development - Video Generation Service**

Implemented the following modules:

1. **Video API Clients** (`src/video/clients.py`)
   - VideoClientBase: Abstract base class
   - VeADKClient: Primary provider with mock mode
   - PikaClient: Backup provider
   - RunwayMLClient: Backup provider
   - Job submission, status polling, result retrieval
   - Automatic fallback between providers

2. **Data Models** (`src/video/models.py`)
   - VideoProvider enum (VEADK, PIKA, RUNWAY)
   - VideoStatus enum (PENDING, PROCESSING, COMPLETED, FAILED)
   - VideoProject with all video metadata
   - CoverStyle enum (BOLD, MINIMAL, COLORFUL, TEXT_HEAVY)

3. **Video Generator** (`src/video/generator.py`)
   - VideoGenerator class
   - Synchronous and asynchronous generation
   - Status checking for existing projects
   - Provider fallback logic
   - Configurable poll interval and timeout

4. **Cover Generator** (`src/video/cover.py`)
   - CoverGenerator class
   - External API integration (DALL-E, Stable Diffusion)
   - Local placeholder generation using PIL
   - Multiple style options
   - Title-based cover generation

5. **Tests** (`tests/test_video.py`)
   - 22 unit tests passing
   - Coverage: models, clients, generator, cover

**Configuration:**
- VEADK_API_KEY, VEADK_BASE_URL
- PIKA_API_KEY, PIKA_BASE_URL
- RUNWAY_API_KEY, RUNWAY_BASE_URL
- COVER_API_KEY, COVER_BASE_URL

**Next Steps:**
- Integrate with PromptGenerator for end-to-end flow
- Add TTS/audio generation for video
- Test with real video generation APIs
- Add video rendering/composition

---

### 2026-03-02 (continued)

**M4 Development - Bilibili Publishing Service**

Implemented the following modules:

1. **OAuth Authentication** (`src/publisher/oauth.py`)
   - BilibiliOAuth class with OAuth 2.0 flow
   - BilibiliToken with expiration management
   - Token file storage and refresh
   - MockBilibiliOAuth for testing without credentials
   - Configuration: BILIBILI_APP_KEY, BILIBILI_APP_SECRET, BILIBILI_REDIRECT_URI

2. **Publish Database** (`src/publisher/database.py`)
   - PublishDatabase class with SQLite
   - PublishRecord model with all metadata
   - PublishStatus enum (PENDING, UPLOADING, UPLOADED, PUBLISHED, FAILED)
   - CRUD operations and statistics

3. **Bilibili Publisher** (`src/publisher/bilibili.py`)
   - BilibiliPublisher class
   - UploadConfig for video metadata
   - VideoCategory enum (10 categories)
   - Video upload with progress callback
   - ScheduledPublisher for automatic publishing

4. **Unit Tests** (`tests/test_publisher.py`)
   - 22 tests passing
   - Coverage: OAuth, database, publisher, scheduler
   - Mock mode for CI/CD testing

**Configuration:**
- BILIBILI_APP_KEY, BILIBILI_APP_SECRET
- BILIBILI_REDIRECT_URI
- BILIBILI_TOKEN_FILE

**Next Steps:**
- Test with real Bilibili API credentials
- Implement actual video upload to Bilibili servers
- Add more error handling and retry logic
- Integrate with video generation pipeline

---

### M5: Data Tracking (Completed ✓)
- [x] M5.1: B站数据 API 接入
  - [x] BilibiliDataClient class (src/tracker/bilibili.py)
  - [x] Get video stats: views, likes, coins, favorites, shares, comments
  - [x] Get粉丝 data: follower count, following count
  - [x] Mock mode for testing
- [x] M5.2: 数据追踪服务
  - [x] DataTracker class (src/tracker/service.py)
  - [x] Track individual videos by BV ID
  - [x] Track all published videos from publish database
  - [x] Track粉丝 data
  - [x] Periodic scheduler with configurable intervals
- [x] M5.3: 数据模型完善
  - [x] VideoStats model (src/tracker/models.py)
  - [x] FansData model
  - [x] GrowthMetrics model
  - [x] TrackedVideo model
  - [x] MetricPeriod enum (DAILY, WEEKLY, MONTHLY)
- [x] M5.4: 单元测试
  - [x] 43 tests passing
  - [x] Coverage: models, client, database, service, scheduler

**Implemented Modules:**

1. **Data Models** (`src/tracker/models.py`)
   - VideoStats: 视频统计数据 (播放、点赞、投币、收藏、分享、评论)
   - FansData: 粉丝数据 (粉丝数、关注数、历史记录)
   - GrowthMetrics: 增长指标 (增长率、播放效率、互动率)
   - TrackedVideo: 被追踪的视频 (含历史数据)
   - MetricPeriod: 时间周期枚举 (DAILY, WEEKLY, MONTHLY)

2. **Bilibili API Client** (`src/tracker/bilibili.py`)
   - BilibiliDataClient: B站数据 API 客户端
   - MockBilibiliDataClient: 测试用模拟客户端
   - 获取视频信息、统计数据、用户信息、粉丝数据

3. **Data Tracker Service** (`src/tracker/service.py`)
   - TrackerDatabase: 追踪数据存储 (JSON 文件)
   - DataTracker: 数据追踪服务
   - 定时拉取已发布视频的数据
   - 定时拉取粉丝数据
   - 计算增长指标
   - MockDataTracker: 测试用模拟追踪器

4. **Unit Tests** (`tests/test_tracker.py`)
   - 43 unit tests passing
   - Coverage: models, client, database, tracker, scheduler

**Configuration:**
- Uses BILIBILI_API_BASE from config
- Data stored in data/tracker_data.json
- Configurable tracking intervals

**Next Steps:**
- Integrate with main pipeline for automatic tracking
- Add data visualization dashboard
- Export reports (CSV/JSON)
- Set up alerts for significant metric changes

---

### M6: Dashboard (Completed ✓)
- [x] M6.1 Dashboard 前端页面
  - [x] 创建 dashboard/ 目录
  - [x] Flask/FastAPI Web UI
  - [x] 展示今日热点 TOP 10
  - [x] 展示已生成 Prompt 列表
  - [x] 展示已发布视频列表
  - [x] 展示数据统计
- [x] M6.2 后端 API
  - [x] Dashboard API (src/dashboard/api.py)
  - [x] /api/dashboard - 总览数据
  - [x] /api/hot-topics - 热点数据
  - [x] /api/videos - 视频列表
  - [x] /api/stats - 统计数据
  - [x] /api/prompts - Prompt 列表
- [x] M6.3 集成测试
  - [x] Dashboard 可正常启动
  - [x] API 端点测试 (11 tests passing)
  - [x] 单元测试覆盖

**Implemented Modules:**

1. **Dashboard API** (`src/dashboard/api.py`)
   - FastAPI 应用
   - 数据模型: HotTopic, PromptItem, VideoItem, StatsData, DashboardData
   - 热点数据接口 (MOCK 数据)
   - 视频列表接口 (从 tracker_data.json 读取)
   - 统计接口 (计算总播放、点赞、投币、收藏、粉丝增长)
   - Prompt 列表接口

2. **Frontend** (`dashboard/index.html`)
   - 现代简约设计
   - 统计卡片 (8 个指标)
   - 热点话题列表 (TOP 10)
   - 已发布视频卡片
   - 已生成 Prompt 列表
   - 自动刷新 (30秒)

3. **Main Entry** (`dashboard_app.py`)
   - 统一入口
   - 同时提供 API 和静态页面服务

4. **Tests** (`tests/test_dashboard.py`)
   - 11 unit tests passing
   - Coverage: 所有 API 端点

**启动方式:**
```bash
python dashboard_app.py
# 访问 http://localhost:5000
```

**API Endpoints:**
- GET / - Dashboard 首页
- GET /api/dashboard - 完整仪表盘数据
- GET /api/hot-topics - 热点话题
- GET /api/videos - 视频列表
- GET /api/stats - 统计数据
- GET /api/prompts - Prompt 列表
