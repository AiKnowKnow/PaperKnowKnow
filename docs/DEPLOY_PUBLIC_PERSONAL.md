# PaperKnowKnow 公网个人版部署说明

这份文档对应当前项目的第一阶段公网方案：

- 一台 Ubuntu 服务器
- FastAPI + Gunicorn
- Nginx 反向代理
- HTTPS（建议用 Let's Encrypt）
- 用户自己填写 AI API Key
- 文件和分析结果保存在服务器本地目录

这不是“多人 SaaS 正式版”，而是“可公网访问的个人版”。

## 1. 适用范围

适合以下场景：

- 你自己长期使用
- 少量熟人一起用
- 先验证网页版体验
- 暂时不做账号系统

暂不适合：

- 大规模公开注册
- 多租户权限隔离
- 平台统一承担 AI 成本

## 2. 服务器要求

建议最低配置：

- Ubuntu 22.04 / 24.04
- 2 vCPU
- 4 GB RAM
- 30 GB SSD

如果 OCR、上传 PDF、AI 分析频率较高，建议再高一点。

## 3. 部署目录建议

```bash
/srv/paper-reader
```

项目数据建议放在：

```bash
/srv/paper-reader/data
```

## 4. 首次部署

### 4.1 安装系统依赖

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip nginx
```

### 4.2 拉取代码

```bash
cd /srv
sudo git clone https://github.com/Dezheng21/paper-reader.git
sudo chown -R $USER:$USER /srv/paper-reader
cd /srv/paper-reader
```

### 4.3 创建虚拟环境并安装依赖

```bash
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt
```

### 4.4 配置环境变量

复制模板：

```bash
cp .env.example .env
```

编辑 `.env`，至少改这些：

```bash
PAPER_ENV=production
PAPER_HOST=0.0.0.0
PAPER_PORT=8000
PAPER_OPEN_BROWSER=false
PAPER_DESKTOP_MODE=false
PAPER_DATA_DIR=/srv/paper-reader/data
PAPER_TRUSTED_HOSTS=your-domain.com,www.your-domain.com
PAPER_CORS_ORIGINS=https://your-domain.com,https://www.your-domain.com
```

## 5. 本机测试启动

```bash
chmod +x scripts/start_public.sh
./scripts/start_public.sh
```

测试健康检查：

```bash
curl http://127.0.0.1:8000/healthz
```

## 6. 配置 systemd

复制服务文件：

```bash
sudo cp deploy/paperknowknow.service /etc/systemd/system/paperknowknow.service
```

如果你的运行用户不是 `www-data`，先修改服务文件里的：

- `User=`
- `Group=`
- `WorkingDirectory=`
- `EnvironmentFile=`
- `ExecStart=`

然后：

```bash
sudo systemctl daemon-reload
sudo systemctl enable paperknowknow
sudo systemctl start paperknowknow
sudo systemctl status paperknowknow
```

## 7. 配置 Nginx

复制模板：

```bash
sudo cp deploy/nginx.paperknowknow.conf /etc/nginx/sites-available/paperknowknow
```

编辑 `server_name` 为你的域名，然后启用：

```bash
sudo ln -s /etc/nginx/sites-available/paperknowknow /etc/nginx/sites-enabled/paperknowknow
sudo nginx -t
sudo systemctl reload nginx
```

## 8. 配置 HTTPS

推荐用 Certbot：

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

## 9. 现在这版的存储方式

当前第一阶段仍然是文件型存储：

- 上传 PDF：`data/uploads/`
- 书架 PDF：`data/library/*.pdf`
- 分析记录：`data/library/*.json`

这对“个人版 / 少量用户”足够。

## 10. 当前第一阶段还没做的事

下面这些是下一阶段再补：

- 用户登录系统
- 数据库（SQLite / Postgres）正式化
- 多用户隔离
- 后台任务队列
- 存储清理策略
- 统一平台 API Key 模式

## 11. 你部署后最先验证的三个点

1. 上传 PDF 是否成功
2. `/analyze` 是否能返回结果
3. 书架保存 / 再打开是否正常

## 12. 常用运维命令

查看服务日志：

```bash
sudo journalctl -u paperknowknow -f
```

重启服务：

```bash
sudo systemctl restart paperknowknow
```

查看健康状态：

```bash
curl http://127.0.0.1:8000/healthz
```

## 13. 当前阶段你需要亲自准备的东西

1. 一台 Ubuntu 服务器
2. 一个域名
3. 服务器 SSH 访问权限
4. 之后你想允许访问的域名列表

如果你准备好了服务器环境，下一步就可以直接开始“按这份文档落地部署”。
