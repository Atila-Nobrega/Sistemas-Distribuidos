async function getDeviceList() {
    try {
        (async () => {
            const rawResponse = await fetch('http://127.0.0.1:8000/dispositivos', {
              method: 'POST',
              headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
              },
              body: JSON.stringify({data: '1|0'})
            });
            const content = await rawResponse.json();

            const devices = content.split('|');
            document.getElementById("sensor_list").innerHTML = "";
            document.getElementById("actuator_list").innerHTML = "";
            devices.forEach(element => {
                const device = JSON.parse(element);

                if(device.nome == "temperatura" || device.nome == "luminosidade" || device.nome == "humidade") {
                    setDeviceListSensor(device.nome, device.id, device.valor)
                }
                else if (device.nome == "Arcondicionado") {
                    setDeviceListArcondicionado(device.nome, device.id, device.valor, device.status)
                } else if (device.nome == "Humidificador") {
                    setDeviceListLHumidificador(device.nome, device.id, device.valor, device.status)
                } else {
                    setDeviceListLampada(device.nome, device.id, device.valor, device.status)
                }
            });
          })();
    } catch (error) {
        console.log(error);
    }

    setTimeout(getDeviceList,2000);
}

function setDeviceListSensor(name, id, value) {
    var block = document.createElement('div');
    block.classList.add('col-md-4');
    block.innerHTML = ""

    image_url = "https://www.kindpng.com/picc/m/562-5627132_device-wireless-wireless-device-icon-png-transparent-png.png"

    //Create Beer Cards inside the HTML Grid.
    block.innerHTML = "<div class=\"card mb-4 shadow-sm\">"
        + "<img class=\"card-img-top\" src=" + image_url + " alt=\"Card image cap\">"
        + "<div class=\"card-body\">"
            + "<h2>"+ name + "</h2>"
            + "<p class=\"card-text\"> Id:" + id + "</p>"
            + "<p class=\"card-text\"> Valor medido:" + value + "</p>"
            + "<div class=\"d-flex justify-content-between align-items-center\">"
            + "<div class=\"d-flex justify-content-between align-items-center\">"
                + "<div class=\"btn-group\">"
                    "<button type=\"button\" class=\"btn btn-sm btn-outline-secondary\">View</button>"
                + "</div>"
            + "</div>"
        + "</div>"
    + "</div>"

    document.getElementById("sensor_list").insertBefore(block, document.getElementById("sensor_list").lastChild);

}

function setDeviceListArcondicionado(name, id, value, status) {
    var block = document.createElement('div');
    block.classList.add('col-md-4');
    block.innerHTML = ""

    image_url = "https://cdn3.iconfinder.com/data/icons/sound-studio-5/64/Actuator-equalizer-switches-controlling-mechanism-512.png"

    //Create Beer Cards inside the HTML Grid.
    block.innerHTML = "<div class=\"card mb-4 shadow-sm\">"
        + "<img class=\"card-img-top\" src=" + image_url + " alt=\"Card image cap\">"
        + "<div class=\"card-body\">"
            + "<h2>"+ name + "</h2>"
            //+ "<p class=\"card-text\"> Id:" + id + "</p>"
            + "<p class=\"card-text\"> Valor Alvo: " + value + "</p>"
            + "<p class=\"card-text\"> Status: " + status + "</p>"
            + "<div class=\"d-flex justify-content-between align-items-center\">"
            + "<div class=\"d-flex justify-content-between align-items-center\">"
                + "<button onClick=\"myFunctionLigarArcondicionado()\">ligar</button>"
                + "<button onClick=\"myFunctionDesligarArcondicionado()\">desligar</button>"
                + "<button onClick=\"myFunctionUpArcondicionado()\">+</button>"
                + "<button onClick=\"myFunctionDownArcondicionado()\">-</button>"
            + "</div>"
        + "</div>"
    + "</div>"

    document.getElementById("actuator_list").insertBefore(block, document.getElementById("actuator_list").lastChild);

}

function setDeviceListLampada(name, id, value, status) {
    var block = document.createElement('div');
    block.classList.add('col-md-4');
    block.innerHTML = ""

    image_url = "https://cdn3.iconfinder.com/data/icons/sound-studio-5/64/Actuator-equalizer-switches-controlling-mechanism-512.png"

    //Create Beer Cards inside the HTML Grid.
    block.innerHTML = "<div class=\"card mb-4 shadow-sm\">"
        + "<img class=\"card-img-top\" src=" + image_url + " alt=\"Card image cap\">"
        + "<div class=\"card-body\">"
            + "<h2>"+ name + "</h2>"
            //+ "<p class=\"card-text\"> Id:" + id + "</p>"
            //+ "<p class=\"card-text\"> Valor Alvo:" + value + "</p>"
            + "<p class=\"card-text\"> Status:" + status + "</p>"
            + "<div class=\"d-flex justify-content-between align-items-center\">"
            + "<div class=\"d-flex justify-content-between align-items-center\">"
                + "<div class=\"d-flex justify-content-between align-items-center\">"
                    + "<button onClick=\"myFunctionLigarLampada()\">ligar</button>"
                    + "<button onClick=\"myFunctionDesligarLampada()\">desligar</button>"
                + "</div>"
            + "</div>"
        + "</div>"
    + "</div>"

    document.getElementById("actuator_list").insertBefore(block, document.getElementById("actuator_list").lastChild);

}

function setDeviceListLHumidificador(name, id, value, status) {
    var block = document.createElement('div');
    block.classList.add('col-md-4');
    block.innerHTML = ""

    image_url = "https://cdn3.iconfinder.com/data/icons/sound-studio-5/64/Actuator-equalizer-switches-controlling-mechanism-512.png"

    //Create Beer Cards inside the HTML Grid.
    block.innerHTML = "<div class=\"card mb-4 shadow-sm\">"
        + "<img class=\"card-img-top\" src=" + image_url + " alt=\"Card image cap\">"
        + "<div class=\"card-body\">"
            + "<h2>"+ name + "</h2>"
            //+ "<p class=\"card-text\"> Id:" + id + "</p>"
            //+ "<p class=\"card-text\"> Valor Alvo:" + value + "</p>"
            + "<p class=\"card-text\"> Status:" + status + "</p>"
            + "<div class=\"d-flex justify-content-between align-items-center\">"
            + "<div class=\"d-flex justify-content-between align-items-center\">"
                + "<div class=\"d-flex justify-content-between align-items-center\">"
                    + "<button onClick=\"myFunctionLigarHumidificador()\">ligar</button>"
                    + "<button onClick=\"myFunctionDesligarHumidificador()\">desligar</button>"
                + "</div>"
            + "</div>"
        + "</div>"
    + "</div>"

    document.getElementById("actuator_list").insertBefore(block, document.getElementById("actuator_list").lastChild);

}

getDeviceList()

function myFunctionLigarArcondicionado() {
    (async () => {
        const rawResponse = await fetch('http://127.0.0.1:8000/dispositivos', {
          method: 'POST',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({data: "2|1"})
        });
        const content = await rawResponse.json();

        console.log(content)
      })();
}

function myFunctionDesligarArcondicionado() {
    (async () => {
        const rawResponse = await fetch('http://127.0.0.1:8000/dispositivos', {
          method: 'POST',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({data: "2|2"})
        });
        const content = await rawResponse.json();

        console.log(content)
      })();
}

function myFunctionUpArcondicionado() {
    (async () => {
        const rawResponse = await fetch('http://127.0.0.1:8000/dispositivos', {
          method: 'POST',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({data: "2|3"})
        });
        const content = await rawResponse.json();

        console.log(content)
      })();
}

function myFunctionDownArcondicionado() {
    (async () => {
        const rawResponse = await fetch('http://127.0.0.1:8000/dispositivos', {
          method: 'POST',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({data: "2|4"})
        });
        const content = await rawResponse.json();

        console.log(content)
      })();
}

function myFunctionLigarLampada() {
    (async () => {
        const rawResponse = await fetch('http://127.0.0.1:8000/dispositivos', {
          method: 'POST',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({data: "3|1"})
        });
        const content = await rawResponse.json();

        console.log(content)
      })();
}

function myFunctionDesligarLampada() {
    (async () => {
        const rawResponse = await fetch('http://127.0.0.1:8000/dispositivos', {
          method: 'POST',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({data: "3|2"})
        });
        const content = await rawResponse.json();

        console.log(content)
      })();
}

function myFunctionLigarHumidificador() {
    (async () => {
        const rawResponse = await fetch('http://127.0.0.1:8000/dispositivos', {
          method: 'POST',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({data: "4|1"})
        });
        const content = await rawResponse.json();

        console.log(content)
      })();
}

function myFunctionDesligarHumidificador() {
    (async () => {
        const rawResponse = await fetch('http://127.0.0.1:8000/dispositivos', {
          method: 'POST',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({data: "4|2"})
        });
        const content = await rawResponse.json();

        console.log(content)
      })();
}
