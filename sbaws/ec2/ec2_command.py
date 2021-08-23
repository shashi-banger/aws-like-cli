

def run_instances(image_id, instance_type, user_data, count):
    print(f"image_id={image_id} instance_type={instance_type}   user_data={user_data}, count={count}")

def terminate_instances(instance_ids, cli_input_json):
    print(f"{instance_ids}, {cli_input_json}")