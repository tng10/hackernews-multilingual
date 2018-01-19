var requested_translations = [];

function resetTranslations(){
	$("table.topstories tbody tr td.title").each(function(index, value){
		$(value).html($(value).data('default'));
	});
}

function checkTranslationsStatus(data, num_items){
	if (data.length > 0 && data.length == num_items) {
		return data.every(function(elem) { return true ? elem.status == 'completed' : false });
	}
	return false;
}

function pollingResultsUnbabel(){
		console.log('polling translations...');
		polling_every = 3000 // milliseconds
		setTimeout(function(){
			if (!is_done) {
		    $.ajax({ 
		    	url: "/api/get-translations/" + requested_translations.join(','), 
		    	contentType:"application/json; charset=utf-8",
		    	dataType: "json",
					success: function(data){
		        is_done = checkTranslationsStatus(data, requested_translations.length);
		        response = data;
		    	}, complete: pollingResultsUnbabel, timeout: 2000
		    });
		  } else {
		  	console.log('translations received...');
		  	translateTitles(response);
		  	cacheTranslations(response);
		  }
		}, polling_every);
}

function translateTitles(data){
	console.log('translating content');
	$.each(data, function(i, v){
		$('*[data-default="' + v.text +'"]').html(v.translatedText);
	});
	console.log('content translated successfully.')
	$(".btn-translating").hide();
}

function requestTranslations(texts, target_lang){
	console.log('requesting translations...');
	$(".btn-translating").show();
	$.ajax({
		  url: "/api/request-translation",
		  type: 'POST',
		  contentType:"application/json; charset=utf-8",
			dataType:"json",
		  data: JSON.stringify({'texts': texts, 'source_lang': 'en', 'target_lang': target_lang})
		}).success(function(data) {
		  is_translated = data['is_translated'];
		  requested_translations = data['results'];
		  console.log('translations requested successfully.');
		  if (is_translated){
		  	console.log('translations were found in cache.');
		  	translateTitles(requested_translations)
		  } else {
			  // start polling results
			  is_done = false;
			  response = [];
				pollingResultsUnbabel();
			}
		});
}

function cacheTranslations(translations){
	console.log('caching translations...');
	$.ajax({
		  url: "/api/cache-translations",
		  type: 'POST',
		  contentType:"application/json; charset=utf-8",
			dataType:"json",
		  data: JSON.stringify(translations)
		}).success(function(data) {
		  console.log('translations cached successfully.');
		});
}