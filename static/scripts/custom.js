function removeTypeaheadBgColorStyle(elementId) {
	if((document.getElementById) && (document.getElementById(elementId) != null)) {
		var element = document.getElementById(elementId);
		// Check the element's style object and background property are available.
	 	if ((element.style)&& (element.style.backgroundColor != null)) {
					element.style.backgroundColor = null;
  		}else {
					// Property is not assigned or is not supported.
					return;
  		}
	} else {
	  	return;
	}
}

// Process data as HTML unordered list.
function getChecklistSubmissions(region, message) {
    if (region.length == 0) {
        return formatResponseMessage(message);
    }

		var url = '/checklists/' + region;
		var data = $.getValues(url, "json");

    return data;
}

function getPreviousRegions(page) {
		var url = '/previous_regions/' + page;
		var data = $.getValues(url, "json");
		return data;
}

function getNotableSightings(region, message) {
    if (region.length == 0) {
        return formatResponseMessage(message);
    }

		var url = '/notables/' + region;
		var data = $.getValues(url, "json");

    return data;
}

function getLocationSubmissions(locationId) {
	if (locationId == "") {
		return "";
	}

	var url = '/location/' + locationId;
	var data = $.getValues(url, "json");

	return data;
}

function getSpeciesSightings(region, fullSpeciesName) {
	if (fullSpeciesName == null) {
		return "";
	}

	var url = '/species/' + region + '/' + fullSpeciesName;
	var data = $.getValues(url, "json");

	return data;
}

function extractErrorMessage(data) {
	return data.slice(data.indexOf('errorMsg":"')+11, data.indexOf('"}]'));
}
// End Data.

// Create output lists.
function getUnorderedList() {
	var ul = document.createElement('ul');
	ul.setAttribute("data-role", "listview");
	ul.setAttribute("class", "ui-listview");
	return ul;
}

function getListItem(innerHtml) {
	var li = document.createElement('li');
	li.setAttribute("class", "ui-li-static ui-body-inherit");
	li.innerHTML = innerHtml;
	return li;
}

function getListItemDivider(innerHtml) {
	var lid = document.createElement('li');
	lid.setAttribute("data-role", "list-divider");
	lid.setAttribute("role", "heading");
	lid.setAttribute("class", "ui-li-divider ui-body-inherit");
	lid.innerHTML = innerHtml;
	return lid;
}

function formatResponseMessage(message) {
	var ul = getUnorderedList();
	ul.appendChild(getListItemDivider(message));
	return ul;
}
// End lists.
