from jinja2 import Template
import os

LAUNCH_TEMPLATE = """<launch>
    <!-- MAVROS node for {{ drone.name }} -->
    <group ns="{{ drone.name }}">
        <node pkg="mavros" type="mavros_node" name="mavros" required="true" clear_params="true">
            <param name="fcu_url" value="udp://:{{ drone.port }}@{{ drone.ip }}:{{ drone.port|int + 1 }}" />
            <param name="gcs_url" value="" />
            <param name="target_system_id" value="{{ drone.id }}" />
            <param name="fcu_protocol" value="v2.0" />
            
            <!-- Параметры для Clover (если используется) -->
            <param name="tgt_system" value="{{ drone.id }}" />
            <param name="pluginlists_yaml" value="$(find mavros)/launch/px4_pluginlists.yaml" />
            <param name="config_yaml" value="$(find mavros)/launch/px4_config.yaml" />
        </node>
    </group>
</launch>
"""

def generate_launch_file(drone):
    template = Template(LAUNCH_TEMPLATE)
    content = template.render(drone=drone)
    
    os.makedirs('launch_files', exist_ok=True)
    with open(f'launch_files/{drone["name"]}.launch', 'w') as f:
        f.write(content)