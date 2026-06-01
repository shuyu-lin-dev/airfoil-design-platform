---
task: T008
scope:
  - POST /geometry/wing-3d 接收 cst_params + wing_planform + structure_design + material_properties
  - 返回 geometry_artifact（format=step, role=structural_step）
  - STEP 覆盖 skin/front_spar/rear_spar/ribs 四组件，保持独立实体
  - 右半翼，span=全展长，chord=恒定弦长，x=弦向/y=厚度/z=展向
  - CAD kernel (cadquery) 生成，禁止手写 STEP
  - 外包盒符合 chord 和 span/2，翼肋数量符合 rib_spacing 规则
  - 蒙皮外表面 CST 截面，内表面固定厚度偏置
  - 梁/肋裁剪在蒙皮内部
validation:
  - cd backend && pytest
exclude:
  - 不返回 1000 个点云
  - 梁/肋与蒙皮内表面精确贴合作几何生成目标，不作为自动测试硬门槛
  - 不生成连接件、开槽、倒角
  - 不生成气动外形 STEP
design_notes:
  - 实现顺序：airfoil wire → face → extrude skin → offset inner → cut → spar boxes → rib boxes → assemble → export STEP
  - 蒙皮厚度固定 0.0015m，前梁 x=0.15 chord，后梁 x=0.70 chord
  - 翼肋：根+尖+均匀间距，数量 ceil(span/2/rib_spacing)+1
