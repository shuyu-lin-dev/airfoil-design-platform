# API Spec (v0.2.0)

## Geometry

### POST /geometry/airfoil-2d
- Request: `{cst_params: [12 floats]}`
- Response: `{points: [{x,y}*200], is_stub, model_version}`

### POST /geometry/wing-3d
- Request: `{cst_params, wing_planform, structure_design, material_properties?}`
- Response: `{geometry_artifact: {artifact_id, format, role, components}, is_stub, model_version}`

## Aerodynamics

### POST /aerodynamics/predict
- Request: `{cst_params, condition: {mach, angle_of_attack}}`
- Response: `{lift_drag_ratio, cp_distribution: [{x,cp}*200], field_artifact, is_stub, model_version}`

## Structure

### POST /structure/predict
- Request: `{cst_params, wing_planform, structure_design, condition, material_properties?}`
- Response: `{max_stress (Pa), weight (N), is_stub, model_version}`

## Optimization

### POST /optimization/aerodynamic
- Request: `{cst_params, condition, target_improvement_ratio}`
- Response: `{original, optimized, actual_improvement_ratio}`

### POST /optimization/structural
- Request: `{cst_params, wing_planform, structure_design, condition, target_reduction_ratio, material_properties?}`
- Response: `{original, optimized, actual_reduction_ratio}`

### POST /optimization/coupled
- Request: `{cst_params, wing_planform, structure_design, condition, target_improvement_ratio, material_properties?}`
- Response: `{original_cst, optimized_cst, original_structure, optimized_structure, actual_improvement_ratio}`

## Artifacts

### GET /artifacts/{artifact_id}
- Response: `{artifact_id, format, role, path, status, datasets?, components?}`

### GET /artifacts/{artifact_id}/download
- Response: binary file (HDF5 or STEP)

## Teaching

### POST /teaching/airfoil-from-control-points
- Request: `{camber_control_points: [{x,y}*2], thickness_control_points: [{x,y}*2]}`
- Response: `{points: [{x,y}*200], is_stub, model_version}`

### POST /teaching/cst-from-airfoil
- Request: `{points: [{x,y}*200]}`
- Response: `{cst_params: [12 floats], is_stub, model_version}`

## Health

### GET /health
- Response: `{status: "ok", version: "0.2.0"}`
