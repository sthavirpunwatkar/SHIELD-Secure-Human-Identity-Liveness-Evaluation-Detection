# SHIELD PR-010E: Comparison Protocol

## Evaluation Architecture 

Pretrained SOTA models must NOT be integrated into the core SHIELD architecture directly. 

The evaluation architecture must follow this strictly isolated bifurcation:

**Path A: External Model Evaluation**
```
Dataset 
   ↓
Adapter (Intercepts and reshapes tensors)
   ↓
External Pretrained Model
   ↓
Metrics
```

**Path B: Internal Baseline Evaluation**
```
Dataset
   ↓
Current SHIELD Production Pipeline
   ↓
Metrics
```

## Scientific Comparison Protocol

The metrics from Path A and Path B are subjected to a **Statistical comparison**.

### Rationale for Pipeline Integrity Preservation

Integrating external pretrained models directly into the production codebase violates the freezing of PR-009. 

1. **Avoidance of Dependency Contamination**: Pulling third-party experimental code, non-standard dependencies, and disparate modeling frameworks into the production environment compromises the stability and security footprint of SHIELD.
2. **Isolation of Preprocessing**: External models rely on radically different preprocessing assumptions (e.g., fixed T frames, different bounding box expansions, specific normalization). Injecting these into the production pipeline creates branching conditional logic that degrades code maintainability.
3. **Purity of Benchmark**: By forcing external models to be run via an Adapter sitting *within the Benchmark Harness* (and outside of SHIELD), we guarantee that the production pipeline is completely untouched. The adapter simply acts as a translation layer between the raw Dataset and the external Model, ensuring the subsequent statistical comparison against the internal SHIELD pipeline is isolated, fair, and secure.
