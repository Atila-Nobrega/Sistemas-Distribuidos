//Request beer list by page
async function getBeerList(page_number) {
    try {
        await fetch('https://api.punkapi.com/v2/beers?page='+ page_number + '&per_page=20')
        .then(response => {
            response.json().then((data) => {
                data.forEach(function selectplaylists(beer) {
                    console.log(beer)
                        setBeerList(beer.name, beer.description, beer.image_url, beer.brewers_tips, beer.contributed_by, beer.tagline, beer.ph, beer.first_brewed, beer.abv, beer.attenuation_level, beer.volume, beer.srm)
                })
            })
        })
    } catch (error) {
        console.log(error)
    }
}

var filter = false //There is a name filter check
var page_number = 1
getBeerList(page_number) // First request when page opens.

//Form submit Script
document.getElementById("searchForm").onsubmit = function() {
    getBeerListByName(document.getElementById("nameSearch").value)
}

//Request Beer list by name
async function getBeerListByName(name_filter) {
    try {
        document.getElementById("beer_list").innerHTML = "";
        if (name_filter == ""){
            filter = false;
            page_number = 1;
            getBeerList(page_number)
        } else {
            filter = true;
            await fetch('https://api.punkapi.com/v2/beers?beer_name=' + name_filter)
            .then(response => {
                response.json().then((data) => {
                    data.forEach(function selectplaylists(beer) {
                            console.log(beer)
                            setBeerList(beer.name, beer.description, beer.image_url, beer.brewers_tips, beer.contributed_by, beer.tagline, beer.ph, beer.first_brewed, beer.abv, beer.attenuation_level, beer.volume, beer.srm)
                    })
                })
            })
        }
    } catch (error) {
        console.log(error)
    }
}

//Set the beer List in the HTML with the returned data.
function setBeerList(name, description, image_url, brewers_tips, contributed_by, tagline, ph, first_brewed, abv, attenuation_level, volume, srm) {
    var block = document.createElement('div');
    block.classList.add('col-md-4');
    block.innerHTML = ""

    //Create Beer Cards inside the HTML Grid.
    block.innerHTML = "<div class=\"card mb-4 shadow-sm\">"
        + "<img class=\"card-img-top\" src=" + image_url + " alt=\"Card image cap\">"
        + "<div class=\"card-body\">"
            + "<h2>"+ name + "</h2>"
            + "<p class=\"card-text\">" + description + "</p>"
            + "<div class=\"d-flex justify-content-between align-items-center\">"
            + "<div class=\"d-flex justify-content-between align-items-center\">"
                + "<div class=\"btn-group\">"
                    "<button type=\"button\" class=\"btn btn-sm btn-outline-secondary\">View</button>"
                + "</div>"
            + "</div>"
        + "</div>"
    + "</div>"

    //Set the modal to open when the Card is clicked.
    block.onclick = () => {
        var modal = document.createElement('div');
        modal.classList.add('modal-content');
        document.getElementById("modal-dialog").innerHTML = "";

        modal.innerHTML = "<div class=\"modal-header\">"
            + "<h3 class=\"modal-title\" id=\"exampleModalLabel\"> <i class=\"inline-icon material-symbols-outlined icon\">sports_bar</i>" + name + "</h3>"
            + "<button type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-label=\"Close\">"
                + "<span aria-hidden=\"true\">&times;</span>"
            + "</button>"
        + "</div>"
        + "<div class=\"modal-body\">"
            + "<h4> <i class=\"inline-icon material-symbols-outlined icon\">label</i>" + tagline + "</h4>"
            + description
            + "<hr>"
            + "<h4> <i class=\"inline-icon material-symbols-outlined icon\">tips_and_updates</i> Brewers tips: </h4>"
            + "<p>" + brewers_tips + "</p>"
            + "<small>-> " + contributed_by + "</small>"
            + "<hr>"
            + "<h4> <i class=\"inline-icon material-symbols-outlined icon\">info</i> Data: </h4>"
            + "<p class =\"dot\"> First Brewed: " + first_brewed + "</p>"
            + "<p class =\"dot\"> Volume: " + volume.value + " " + volume.unit + "</p>"
            + "<p class =\"dot\"> ABV: " + abv + "</p>"
            + "<p class =\"dot\"> Attenuation level: " + attenuation_level + "</p>"
            + "<p class =\"dot\"> Standard Research Method: " + srm + "</p>"
            + "<p class =\"dot\"> pH Level: " + ph + "</p>"
        + "</div>"


        document.getElementById("modal-dialog").insertBefore(modal, document.getElementById("modal-dialog").firstChild);

        $('#exampleModal').modal('show');
    };

    document.getElementById("beer_list").insertBefore(block, document.getElementById("beer_list").lastChild);

}

//Loads more beers when the page scrolls to the bottom.
$(window).scroll(function () {
    if ($(document).height() <= $(window).scrollTop() + $(window).height()) {
        if (filter) {
            
        }
        else {
            window.scrollBy(0,-200)
            page_number = page_number + 1
            getBeerList(page_number)
        }
    }
});

var form = document.getElementById("searchForm");
function handleForm(event) { event.preventDefault(); } 
form.addEventListener('submit', handleForm);