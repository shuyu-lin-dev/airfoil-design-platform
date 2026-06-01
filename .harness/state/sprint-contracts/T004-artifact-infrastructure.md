---
task: T004
title: Artifact infrastructure with HDF5 store
scope:
  - artifact_id 生成：输入参数字典规范化 JSON 序列化后 SHA-256 前 12 字符
  - hdf5_store：写入 HDF5 文件到 runtime_artifacts/aerodynamic/<id>.h5，同步写 JSON sidecar
  - artifact_registry：通过 artifact_id 查询已注册 artifact 的元信息（从 sidecar 读取）
  - HDF5 dataset 布局：/coordinates (1000,2)、/fields/pressure (1000,)、/fields/velocity (1000,)
  - 测试为纯 Python 单元测试，不依赖 HTTP API
validation:
  commands:
    - cd backend && pytest
exclusions:
  - 不涉及 HTTP API（留给 T005）
  - 不涉及 STEP 存储（留给 T007）
  - 不生成真实气动数据，测试使用合成 numpy 数组
observable_signals:
  - pytest 全部通过
  - HDF5 文件可被 h5py 回读，dataset shape 和 dtype 符合预期
  - JSON sidecar 存在且包含 artifact_id、format、role、path、status、datasets
  - artifact_registry.get(id) 返回完整元信息
