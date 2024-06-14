
function infogeo(){

  var _e;
  for ( _e = 1 ; _e < 33 ; _e ++ ){
    $('#infogeo-entidad').append($('<option>', {
      value: _e,
      text : ui.get_entidad( _e ).name
    }));
  }

  $( "#infogeo-titulo" ).html( __site.crumb );
  switch (__lugar){
    case 'CG':
      // Condensado General
      $( "#infogeo-descripcion" ).html("Aquí se enlista el Concentrado general de distritos, municipios, secciones, localidades y manzanas por entidad.");

      $( "#area-infogeo-descarga" ).show();

      var url = aajax__ + 'infogeo/get_cgdmslm.php';
      $.ajax( url, {cache: false, async: false, method: "POST"} )
        .then( function( data ){
        if (data.ok){
          var info = (data);
          // console.log(info);
          ui.mustache.render( 'infogeo-cgdmslm-tabla', info , 'area-infogeo-tabla' );
          ui.mustache.render( 'infogeo-corte', info , 'area-infogeo-corte' );
          ui.mustache.render( 'infogeo-cgdmslm-footer', info , 'area-infogeo-footer' );
        }
      } );
      $( ".toogle-columns" ).click(function(e) {
        e.preventDefault();
        if ( $(this).data('col') == $(this).data('max') ){
          $(this).attr('colspan', $(this).data('min') );
          $( "." + $(this).data('class') ).hide();
          $(this).data('col', $(this).data('min') );
        }else{
          $(this).attr('colspan', $(this).data('max') );
          $( "." + $(this).data('class') ).show();
          $(this).data('col', $(this).data('max') );
        }
      } );
		// $("#infogeo-cgdmslm-descarga")
    break;
    case 'CGS':
      $( "#infogeo-descripcion" ).html("Aquí puedes consultar el Concentrado General de Secciones Electorales por Distrito y Municipio, Filtrado a Nivel Entidad.");

      $( "#area-infogeo-entidad" ).show();

      $( "#infogeo-entidad" ).change(function() {
        var ent = $(this).val();

        var parametro = { e : ent };
        var url = aajax__ + 'infogeo/get_cgs.php';
        $.ajax( url, {cache: false, async: false, method: "POST", data: parametro} )
          .then( function( data ){
          if ( data.ok ){
            // console.log(data);
            data.ne = ui.get_entidad(ent).name;
            ui.mustache.render( 'infogeo-cgs-tabla', data , 'area-infogeo-tabla' );
            ui.mustache.render( 'infogeo-corte', data , 'area-infogeo-corte' );
          }
        } );

      });


    break;
    case 'RSM':

      $( "#infogeo-descripcion" ).html("Aquí podras consultar el Catalogo de Rango de Secciones Electorales por Municipio, Filtrado a Nivel Entidad.");

      $( "#area-infogeo-entidad" ).show();

      $( "#infogeo-entidad" ).change(function() {
        var ent = $(this).val();

        var parametro = { e : ent };
        var url = aajax__ + 'infogeo/get_rsm.php';
        $.ajax( url, {cache: false, async: false, method: "POST", data: parametro} )
          .then( function( data ){
          if (data.ok){
            var info = (data);
            info.ne = ui.get_entidad(ent).name;
            info.e = ent;
            // console.log(info);
            ui.mustache.render( 'infogeo-rsm-tabla', info , 'area-infogeo-tabla' );
            ui.mustache.render( 'infogeo-corte', info , 'area-infogeo-corte' );
          }
        } );

      });

    break;
  }
  $( "#area-infogeo-descarga" ).show();
  $(".infogeo-descarga").on("click", infgeo_descargas );
  var options = {
    toggle : "popover" ,
    trigger : "hover"
    };
  $('.info-popover').popover(options);

  // Aquí vamos a poner el evento de carga.
  if ( (__edms.e != 'undefined') && (__edms.e > 0) )
    $('#infogeo-entidad').val( __edms.e ).change();
}
function infgeo_descargas(){

  switch (__lugar){
    case 'CG':
      var url = aajax__ + 'infogeo/down_cgdmslm.php';
    break;
    case 'CGS':
    		var url = aajax__ + 'infogeo/down_cgs.php';
    break;
    case 'RSM':
    		var url = aajax__ + 'infogeo/down_rgs.php';
    break;
  }
  // console.log('Download: ' + __lugar + ' ' + url);
  var caracteristicas = 'height=300,width=300,scrollTo,resizable=1,scrollbars=1,location=0';
	var nueva = window.open(url,'Descarga de información geografica.',caracteristicas);
}
