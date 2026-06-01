---
task: T006
scope:
  - POST /aerodynamics/predict 接收 cst_params(12 floats) + condition(mach, angle_of_attack)，返回 lift_drag_ratio + 200 Cp 点 + field_artifact 引用
  - Cp 分布与翼型点按索引一一对应（200 个点）
  - 压力场和速度场写入 HDF5 artifact（1000 点 /coordinates + /fields/pressure + /fields/velocity），不通过 JSON 返回
  - HDF5 + JSON sidecar 同步落盘，artifact_id 由输入参数确定性生成
  - 响应包含 is_stub: true, model_version: "stub-v0"
  - 遵循架构边界：api 不写业务逻辑，core 不依赖具体实现类，lib 不依赖业务层
validation:
  - cd backend && pytest
exclude:
  - 不使用真实 CFD 求解器（全部 stub 占位算法）
  - 不验证气动计算结果物理合理性
  - 不提供模型版本选择（仅 stub-v0）
  - HDF5 dataset 布局固定（1000 点），不可配置
design_notes:
  - Stub 升阻比：基于 camber + AOA 的简单参数化公式
  - Stub Cp：基于翼型点 x 坐标的线性衰减
  - Stub 场数据：40×25 矩形网格覆盖翼型区域，pressure/velocity 基于到最近翼型点距离的衰减函数
  - 场坐标生成在 core/ 层为纯函数，不依赖 CAD kernel 或外部 solver
