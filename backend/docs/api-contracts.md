# API Contracts

## Common Models

### ConditionParams
- `mach`: float, dimensionless
- `angle_of_attack`: float, degree

### WingPlanform
- `span`: float, m, default 10.0, range (0, 100]
- `chord`: float, m, default 1.0, range (0, 20]

### StructureDesign
- `rear_spar_web_thickness`: float, m, range [0.002, 0.020]
- `rib_thickness`: float, m, range [0.002, 0.005]
- `rib_spacing`: float, m, range [0.300, 1.000]

### MaterialGroup
- `elastic_modulus`: float, Pa, must be positive
- `material_density`: float, kg/m³, must be positive

### MaterialProperties
- `skin`: Optional[MaterialGroup], default aluminum (70 GPa, 2700 kg/m³)
- `internal_structure`: Optional[MaterialGroup], default steel (200 GPa, 7850 kg/m³)

## Defaults

| Parameter | Value |
|-----------|-------|
| Wing span | 10.0 m |
| Wing chord | 1.0 m |
| Skin thickness | 0.0015 m (fixed) |
| Front spar chord position | 0.15 (fixed) |
| Rear spar chord position | 0.70 (fixed) |
| Front spar thickness | rear_spar_web_thickness × 1.5 |
| Gravity | 9.8 m/s² |
