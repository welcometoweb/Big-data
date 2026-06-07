const API_URL = "YOUR_APPS_SCRIPT_URL";

let selectedType = "Need";

const successMessages = [
    "💸 Money remembered",
    "🧾 Expense captured",
    "📒 Added to ledger",
    "🚀 Budget updated",
    "✅ Logged successfully"
];

document.addEventListener("DOMContentLoaded", () => {

    updateGreeting();

    document
        .querySelectorAll(".type-btn")
        .forEach(btn => {

            btn.addEventListener("click", () => {

                document
                    .querySelectorAll(".type-btn")
                    .forEach(b => b.classList.remove("active"));

                btn.classList.add("active");

                selectedType = btn.dataset.type;
            });
        });
});

function updateGreeting(){

    const hour = new Date().getHours();

    let greeting = "";

    if(hour < 12){
        greeting = "☀️ Good Morning";
    }
    else if(hour < 18){
        greeting = "🌤 Good Afternoon";
    }
    else{
        greeting = "🌙 Good Evening";
    }

    document.getElementById("greeting").innerText = greeting;
}

async function saveExpense(){

    const amount =
        document.getElementById("amount").value;

    if(!amount){

        alert("Enter amount");

        return;
    }

    const payload = {

        person:
            document.getElementById("person").value,

        category:
            document.getElementById("category").value,

        amount,

        paymentMode:
            document.getElementById("paymentMode").value,

        type: selectedType,

        notes:
            document.getElementById("notes").value
    };

    const status =
        document.getElementById("status");

    status.innerText = "Saving...";

    try{

        const response =
            await fetch(API_URL,{
                method:"POST",
                body:JSON.stringify(payload)
            });

        const result =
            await response.json();

        if(result.success){

            const message =
                successMessages[
                    Math.floor(
                        Math.random() *
                        successMessages.length
                    )
                ];

            status.innerText = message;

            document
                .getElementById("lastExpense")
                .innerText =
                `Last: ${payload.category} • ₹${payload.amount}`;

            document
                .getElementById("amount")
                .value = "";

            document
                .getElementById("notes")
                .value = "";
        }

    }catch(error){

        status.innerText =
            "❌ Could not save";
    }
}