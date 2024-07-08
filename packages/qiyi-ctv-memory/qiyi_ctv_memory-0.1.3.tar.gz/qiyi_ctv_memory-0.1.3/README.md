# 发布流程

1. 修改 `setup.py` 中的版本号
2. 清理 `qiyi_ctv_memory.egg-info` 目录及 `dist` 目录
3. 运行 `python setup.py sdist bdist_wheel`
4. 使用 Twine 上传包 `twine upload -u __token__ -p "YOUR_PYPI_API_TOKEN" dist/*`

# 安装


```sh
pip install qiyi_ctv_memory
```

# 升级

```sh
pip install --upgrade qiyi_ctv_memory
```

# 发布前置安装

1. 安装 setuptools 和 wheel:

```sh
pip install setuptools wheel
```

2. 安装 Twine:

```sh
pip install twine
```