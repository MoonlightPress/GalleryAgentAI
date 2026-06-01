
import subprocess, sys
scripts=[
'publisher_ecosystem_builder_v1.py',
'publisher_verifier_v1.py',
'alternative_space_builder_v1.py',
'gallery_cleanup_layer_v1.py',
'master_opportunity_schema_v1.py',
'category_summary_generator_v1.py'
]
for s in scripts:
    subprocess.run([sys.executable,s], check=True)
print('OPPORTUNITY EXPANSION SPRINT V1 COMPLETE')
