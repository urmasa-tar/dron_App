from jinja2 import Template
import os

LAUNCH_TEMPLATE = """<?xml version="1.0"?>
<launch>
    <!-- MAVROS node for {{ drone.name }} -->
    <node pkg="mavros" type="mavros_node" name="{{ drone.node_name }}" output="screen">
        <param name="fcu_url" value="{{ drone.fcu_url }}" />
        <param name="target_system_id" value="{{ drone.system_id }}" />
        <param name="fcu_protocol" value="v2.0" />
    </node>
</launch>
"""

def generate_launch_file(drone):
    template = Template(LAUNCH_TEMPLATE)
    content = template.render(drone=drone)
    
    os.makedirs('launch_files', exist_ok=True)
    with open(f'launch_files/{drone["name"]}.launch', 'w', encoding='utf-8') as f:
        f.write(content)