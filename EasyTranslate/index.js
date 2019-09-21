const translate = require('@k3rn31p4nic/google-translate-api');

var sentence = 'Rolling processing is known as a surface strengthening process. Under the action of rolling and extrusion, plastic deformation occurs on the surface of the material, which will lead to grain refinement, dislocation configuration and phase change.  '


document.getElementById('clickEE').addEventListener("click",function(){
    var text = document.getElementById('source');
    var sentence = text.value;
    
    translate(sentence, { from: 'en', to: 'zh-cn' }).then(res => { 
        var result = res.text;
        return result;
    })
    .then(result2 => {
        translate(result2,{ from: 'zh-cn', to: 'en' }).then(res =>
            {
            document.getElementById('translated').innerHTML = res.text;
            })
    })
    .catch(err => {
     console.error(err);
     document.getElementById('translated').innerHTML = err;
    });
    })
    
document.getElementById('clickEZ').addEventListener("click", function () {
    var text = document.getElementById('source');
    var sentence = text.value;

    translate(sentence, { to: 'zh-cn' }).then(res => {
        document.getElementById('translated').innerHTML = res.text;
    }).catch(err => {
            console.error(err);
            document.getElementById('translated').innerHTML = err;
        });
})

document.getElementById('clickZE').addEventListener("click", function () {
    var text = document.getElementById('source');
    var sentence = text.value;

    translate(sentence, { to: 'en' }).then(res => {
        document.getElementById('translated').innerHTML = res.text;
    }).catch(err => {
            console.error(err);
            document.getElementById('translated').innerHTML = err;
        });
})
