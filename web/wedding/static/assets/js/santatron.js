(function($) {

	var app = $.sammy('#main', function() {
		this.use('Template');
		this.get('#/', function(context) {
			 context.render('/static/assets/templates/item.template')
               .appendTo(context.$element());
		});

	});

	$(function() {
		app.run('#/');
	});

 })(jQuery);
