# Mesh Layer — Architecture (Task 1)

## Scope boundary
The Mesh layer's pipeline begins only after Backend hands it a generated
mesh file/reference produced by the AI layer's reconstruction model.
The Mesh layer does not perform image classification, model selection,
or confidence prediction (AI layer's responsibility). It never calls
the AI layer directly and never writes to the database directly —
all persistence goes through Backend.

## Pipeline stages (future tasks, referenced here for context)
Backend -> Mesh Ingestion -> Mesh Analysis -> Mesh Quality Evaluation
-> Repair -> Optimization -> Texture/Material -> Export/Blender/AR/Printing
-> results returned to Backend

## Environment
Python 3.10 (venv), Open3D 0.18.0, Trimesh 4.4.9, PyMeshLab 2023.12.post1,
NumPy 1.26.4. Pinned due to Open3D/PyMeshLab compatibility limits on
newer Python versions (see requirements.txt).