var page = require('webpage').create(),
    address, output, size;

if (phantom.args.length < 2 || phantom.args.length > 3) {
    console.log('Usage: rasterize.js URL filename');
    phantom.exit();
} else {
    address = phantom.args[0];
    output = phantom.args[1];

    page.open(address, function (status) {
        if (status !== 'success') {
            console.log('Unable to load the address!');
            phantom.exit();
        } else {
            var dimension = page.evaluate(function () {
                document.body.style.webkitTransform = "scale(2)";
                document.body.style.webkitTransformOrigin = "0% 0%";
                /* fix the body width that overflows out of the viewport */
                document.body.style.width = "50%";

                return {
                    width:parseInt(document.getElementById('mindmap-map').getAttribute('data-dimension-left'))*5,
                    height:parseInt(document.getElementById('mindmap-map').getAttribute('data-dimension-top'))*5
                };
            });
            window.setTimeout(function () {
                page.paperSize = dimension;
                page.render(output);
                phantom.exit();
            }, 2000);
        }
    });
}