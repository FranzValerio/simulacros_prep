
var distritacion = function (__void) {
  var od = {};
  // console.log( __lugar  );
  od.init = function (__param) {
    console.log(__param, __lugar, __sitio);

    switch (__lugar) {
      case 'local':
        // encabezados de lo federal:
        ui.mustache.render('mu-dttoloc-title', {}, 'area-distritacion-titulo');
        ui.mustache.render('mu-dttoloc-foot', {}, 'area-distritacion-pie');

        var url = aajax__ + 'distritacion/local.php';
        $.ajax(url, { cache: false, async: true, method: "POST", data: { servicio: 'local' } })
          .then(function (data) {
            ui.mustache.render('mu-dttoloc-table', data, 'area-distritacion-tabla');
          });

        break;
      case 'federal':
        // encabezados de lo federal:
        ui.mustache.render('mu-dttofed-title', {}, 'area-distritacion-titulo');
        ui.mustache.render('mu-dttofed-foot', {}, 'area-distritacion-pie');

        var url = aajax__ + 'distritacion/federal.php';
        $.ajax(url, { cache: false, async: true, method: "POST", data: { servicio: 'federal' } })
          .then(function (data) {
            ui.mustache.render('mu-dttofed-table', data, 'area-distritacion-tabla');
          });
        break;
      case 'acuerdos':
        // encabezados de lo federal:
        if (__sitio == "distritacion2021") {
          ui.mustache.render('mu-acuerdos21-title', {}, 'area-distritacion-titulo');
          // ui.mustache.render( 'mu-acuerdos21-foot', {} , 'area-distritacion-pie' );
          var url = aajax__ + 'distritacion/acuerdos2021.php';
          $.ajax(url, { cache: false, async: true, method: "POST", data: { servicio: 'acuerdos' } })
            .then(function (data) {
              ui.mustache.render('mu-acuerdos21-table', data, 'area-distritacion-tabla');
            });
        } else {
          ui.mustache.render('mu-acuerdos-title', {}, 'area-distritacion-titulo');
          ui.mustache.render('mu-acuerdos-foot', {}, 'area-distritacion-pie');
          var url = aajax__ + 'distritacion/acuerdos.php';
          $.ajax(url, { cache: false, async: true, method: "POST", data: { servicio: 'acuerdos' } })
            .then(function (data) {
              ui.mustache.render('mu-acuerdos-table', data, 'area-distritacion-tabla');
            });
        }
        break;
      case 'numeralia':
        // encabezados de lo federal:
        ui.mustache.render('mu-numeralia-title', {}, 'area-distritacion-titulo');
        ui.mustache.render('mu-numeralia-foot', {}, 'area-distritacion-pie');
        var url = aajax__ + 'distritacion/numeralia.php';
        $.ajax(url, { cache: false, async: true, method: "POST", data: { servicio: 'numeralia' } })
          .then(function (data) {
            ui.mustache.render('mu-numeralia-table', data, 'area-distritacion-tabla');
          });
        break;
      case 'eceg':
        // encabezados de lo federal:
        ui.mustache.render('mu-eceg-title', {}, 'area-distritacion-titulo');
        // ui.mustache.render( 'mu-eceg-foot', {} , 'area-distritacion-pie' );
        var url = aajax__ + 'distritacion/eceg.php';
        // alert(url);
        $.ajax(url, { cache: false, async: true, method: "POST", data: { servicio: 'eceg' } })
          .then(function (data) {
            ui.mustache.render('mu-eceg-table', data, 'area-distritacion-tabla');
          });
        break;
    };
    console.log(__lugar);
  };
  od.show = function (parametro) {

    alert(parametro + __lugar + __sitio);

    return false;
  };

  return od;
};
