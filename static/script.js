const API_URL = "http://127.0.0.1:8000/api";

const carsContainer = document.getElementById("cars_container");
const searchInput = document.getElementById("search_input");

function renderCar(car) {
    return `
        <div class="col-md-4 mb-4">
            <div class="card">
                <div class="card-body">
                    <h4 class="card-title">${car.firm} ${car.model}</h4>
                    <p class="card-text">
                        <strong>Год:</strong> ${car.year}<br>
                        <strong>Мощность:</strong> ${car.power} л.с.<br>
                        <strong>Цвет:</strong> ${car.color}<br>
                        <strong>Цена:</strong> $${car.price}
                    </p>
                </div>
                <div class="card-footer d-flex justify-content-between">
                    <button class="btn btn-warning btn-sm" onclick="openEditModal(${car.id})">
                        Редактировать
                    </button>
                    <button class="btn btn-danger btn-sm" onclick="openDeleteModal(${car.id}, '${car.firm} ${car.model}')">
                        Удалить
                    </button>
                </div>
            </div>
        </div>
    `;
}

async function loadCars() {
    carsContainer.innerHTML = "";
    try {
        const response = await fetch(`${API_URL}/cars/`);
        const cars = await response.json();

        cars.forEach(car => {
            carsContainer.innerHTML += renderCar(car);
        });
    } catch (error) {
        alert("Ошибка загрузки автомобилей");
        console.error(error);
    }
}

async function findCarById() {
    const id = searchInput.value;
    if (!id) return;

    carsContainer.innerHTML = "";
    try {
        const response = await fetch(`${API_URL}/cars/${id}`);
        if (!response.ok) {
            switch (response.status) {
                case 404: alert("Автомобиль с таким ID не найден"); break;
                case 422: alert("ID указан неверно"); break;
            }
            await loadCars();
            return;
        }

        const car = await response.json();
        carsContainer.innerHTML += renderCar(car);

    } catch(error) {
        alert("Ошибка поиска");
        console.error(error);
    } finally {
        searchInput.value = "";
    }
}

let deleteCarId = null;
let deleteModal;

function openDeleteModal(id, name) {
    deleteCarId = id;
    document.getElementById("delete_car_name").textContent = name;

    deleteModal = new bootstrap.Modal(document.getElementById("delete_modal"));
    deleteModal.show();
}

async function deleteCar() {   
    try {
        await fetch(`${API_URL}/cars/${deleteCarId}`, {
            method: "DELETE"
        })

        deleteModal.hide();
        loadCars();
    } catch(error) {
        alert("Ошибка удаления");
        console.error(error);
    }
}

let modal;

function openEditModal(id) {
    try {
        fetch(`${API_URL}/cars/${id}`)
            .then(response => response.json())
            .then(car => {
                Object.keys(car).forEach(
                    key => document.getElementById(`edit_${key.replace("_id", "")}`).value = car[key]
                );
            });
        modal = new bootstrap.Modal(document.getElementById("edit_modal"));
        modal.show(); 
    } catch(error) {
        alert("Ошибка обновления");
        console.error(error);
    }
}

async function saveChanges() {
    try {
        const id = document.getElementById("edit_id").value;

        const car = {
            firm: document.getElementById("edit_firm").value,
            model: document.getElementById("edit_model").value,
            year: document.getElementById("edit_year").value,
            power: document.getElementById("edit_power").value,
            color: document.getElementById("edit_color").value,
            price: document.getElementById("edit_price").value,
            dealer_id: document.getElementById("edit_dealer").value
        };

        await fetch(`${API_URL}/cars/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(car)
        });

        modal.hide();
        loadCars();
    } catch (error) {
        alert("Ошибка сохранения изменений");
        console.error(error);
    }
}

loadCars();