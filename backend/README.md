# Airfoil Design Platform Backend

翼型气动与强度智能设计平台后端 MVP。

## 安装

```bash
python3.10 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,cad]"
```

## 启动

```bash
source .venv/bin/activate
uvicorn airfoil_platform.main:app --reload
```

## 测试

```bash
source .venv/bin/activate
pytest
```
