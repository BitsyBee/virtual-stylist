async function login() {

const email = document.getElementById("email").value.trim();
const password = document.getElementById("password").value;

const loginResult = document.getElementById("loginResult");

if (!email || !password) {
    loginResult.innerText = "Please enter email and password.";
    return;
}

try {

    const response = await fetch(
        "http://127.0.0.1:8001/login",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                email: email,
                password: password
            })
        }
    );

    const data = await response.json();

    if (!response.ok) {

        loginResult.innerText =
            data.detail || "Login failed.";

        return;
    }

    if (!data.access_token) {

        loginResult.innerText =
            data.message || "Invalid credentials.";

        return;
    }

    localStorage.setItem(
        "access_token",
        data.access_token
    );

    loginResult.innerText =
        "Login successful!";

    document.getElementById(
        "loginSection"
    ).style.display = "none";

    document.getElementById(
        "stylistSection"
    ).style.display = "block";

    document.getElementById(
    "profileSection"
).style.display = "block";

loadProfile();

} catch (error) {

    console.error("Login error:", error);

    loginResult.innerText =
        "Could not connect to the API.";
}


}



 async function getRecommendation() {


const message = document.getElementById("userMessage").value.trim();
const result = document.getElementById("result");

if (!message) {
    result.innerHTML =
        "<p>Please tell me what you are dressing for.</p>";
    return;
}

result.innerHTML =
    "<p>Finding the best outfits...</p>";

const text = message.toLowerCase();

// ------------------------------------------------
// DEFAULT VALUES
// ------------------------------------------------

let occasion = "Casual Outing";
let style = "Casual";
let temperature = "Warm";
let season = "All Season";


// ------------------------------------------------
// OCCASION + STYLE
// ------------------------------------------------

if (
    text.includes("job interview") ||
    text.includes("interview")
) {

    occasion = "Interview";
    style = "Formal";

} else if (
    text.includes("office") ||
    text.includes("work")
) {

    occasion = "Office";
    style = "Formal";

} else if (
    text.includes("presentation") ||
    text.includes("presenting")
) {

    occasion = "Presentation";
    style = "Formal";

} else if (
    text.includes("party") ||
    text.includes("birthday")
) {

    occasion = "Party";
    style = "Casual";

} else if (
    text.includes("university") ||
    text.includes("campus") ||
    text.includes("lecture")
) {

    occasion = "University";
    style = "Casual";

} else if (
    text.includes("sport") ||
    text.includes("gym") ||
    text.includes("football") ||
    text.includes("cricket")
) {

    occasion = "Sports";
    style = "Sport";

} else if (
    text.includes("casual outing") ||
    text.includes("going out") ||
    text.includes("hangout") ||
    text.includes("hanging out")
) {

    occasion = "Casual Outing";
    style = "Casual";
}


// ------------------------------------------------
// EXPLICIT STYLE
// ------------------------------------------------

if (
    text.includes("formal") ||
    text.includes("professional") ||
    text.includes("business")
) {

    style = "Formal";

} else if (
    text.includes("smart casual")
) {

    style = "Smart Casual";

} else if (
    text.includes("sporty") ||
    text.includes("sportswear")
) {

    style = "Sport";

} else if (
    text.includes("casual")
) {

    style = "Casual";
}


// ------------------------------------------------
// TEMPERATURE
// ------------------------------------------------

if (
    text.includes("very hot") ||
    text.includes("extremely hot") ||
    text.includes("boiling") ||
    text.includes("scorching")
) {

    temperature = "Hot";

} else if (
    text.includes("hot") ||
    text.includes("humid") ||
    text.includes("heat") ||
    text.includes("really warm")
) {

    temperature = "Hot";

} else if (
    text.includes("very cold") ||
    text.includes("extremely cold") ||
    text.includes("freezing")
) {

    temperature = "Cold";

} else if (
    text.includes("cold") ||
    text.includes("chilly") ||
    text.includes("cool")
) {

    temperature = "Cold";

} else if (
    text.includes("warm")
) {

    temperature = "Warm";
}


// ------------------------------------------------
// SEASON
// ------------------------------------------------

if (
    text.includes("summer")
) {

    season = "Summer";

} else if (
    text.includes("winter")
) {

    season = "Winter";

} else if (
    text.includes("spring")
) {

    season = "Spring";

} else if (
    text.includes("autumn") ||
    text.includes("fall")
) {

    season = "Autumn";
}


// ------------------------------------------------
// DEBUG INFORMATION
// ------------------------------------------------

console.log("User message:", message);
console.log("Detected occasion:", occasion);
console.log("Detected style:", style);
console.log("Detected temperature:", temperature);
console.log("Detected season:", season);


// ------------------------------------------------
// CHECK LOGIN
// ------------------------------------------------

try {

    const token =
        localStorage.getItem("access_token");

    if (!token) {

        result.innerHTML =
            "<p>Please login first.</p>";

        return;
    }


    // ------------------------------------------------
    // SEND TO BACKEND
    // ------------------------------------------------

    const response = await fetch(
        "http://127.0.0.1:8001/recommendation/",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },

            body: JSON.stringify({
                occasion: occasion,
                style: style,
                temperature: temperature,
                season: season
            })
        }
    );


    const data = await response.json();


    // ------------------------------------------------
    // HANDLE ERROR
    // ------------------------------------------------

    if (!response.ok) {

        console.error(data);

        result.innerHTML =
            "<p>Something went wrong while getting recommendations.</p>";

        return;
    }


    // ------------------------------------------------
    // DISPLAY RESULTS
    // ------------------------------------------------

    displayRecommendations(data);

} catch (error) {

    console.error(
        "Recommendation error:",
        error
    );

    result.innerHTML =
        "<p>Could not connect to the Virtual Stylist API.</p>";
}


}



function displayRecommendations(outfits) {

    const result = document.getElementById("result");

    if (!Array.isArray(outfits) || outfits.length === 0) {
        result.innerHTML = `
            <div class="no-results">
                <h2>No suitable outfits found</h2>
                <p>Try changing your occasion, style, temperature, or season.</p>
            </div>
        `;
        return;
    }

    let html = `
        <div class="recommendation-header">
            <h2>Recommended Outfits</h2>
            <p>Personalized selections based on your profile and request.</p>
        </div>
    `;

    outfits.forEach((outfit) => {

        const allReasons = [
            ...outfit.top.reasons,
            ...outfit.bottom.reasons,
            ...outfit.shoes.reasons,
            ...outfit.compatibility_reasons
        ];

        const uniqueReasons = [...new Set(allReasons)];

        html += `
            <div class="outfit-card">

                <div class="outfit-header">

                    <div>
                        <h3>Outfit #${outfit.rank}</h3>
                        <p>Complete outfit recommendation</p>
                    </div>

                    <div class="score">
                        <span>${outfit.score}</span>
                        <small>Score</small>
                    </div>

                </div>


                <div class="outfit-items">

                    <!-- TOP -->

                    <div class="clothing-item">

                        <div class="item-image-container">

                            <img
                                src="http://127.0.0.1:8001/${outfit.top.image_url}"
                                alt="${outfit.top.name}"
                                class="clothing-image"
                            >

                        </div>

                        <div class="item-details">

                            <span class="item-category">
                                TOP
                            </span>

                            <h4>
                                ${outfit.top.name}
                            </h4>

                            <p>
                                ${outfit.top.color} ·
                                ${outfit.top.style}
                            </p>

                        </div>

                    </div>


                    <!-- BOTTOM -->

                    <div class="clothing-item">

                        <div class="item-image-container">

                            <img
                                src="http://127.0.0.1:8001/${outfit.bottom.image_url}"
                                alt="${outfit.bottom.name}"
                                class="clothing-image"
                            >

                        </div>

                        <div class="item-details">

                            <span class="item-category">
                                BOTTOM
                            </span>

                            <h4>
                                ${outfit.bottom.name}
                            </h4>

                            <p>
                                ${outfit.bottom.color} ·
                                ${outfit.bottom.style}
                            </p>

                        </div>

                    </div>


                    <!-- SHOES -->

                    <div class="clothing-item">

                        <div class="item-image-container">

                            <img
                                src="http://127.0.0.1:8001/${outfit.shoes.image_url}"
                                alt="${outfit.shoes.name}"
                                class="clothing-image"
                            >

                        </div>

                        <div class="item-details">

                            <span class="item-category">
                                SHOES
                            </span>

                            <h4>
                                ${outfit.shoes.name}
                            </h4>

                            <p>
                                ${outfit.shoes.color} ·
                                ${outfit.shoes.style}
                            </p>

                        </div>

                    </div>

                </div>


                <!-- WHY THIS OUTFIT -->

                <div class="reasons">

                    <h4>
                        Why this outfit?
                    </h4>

                    <ul>

                        ${uniqueReasons
                            .map(reason => `
                                <li>${reason}</li>
                            `)
                            .join("")}

                    </ul>

                </div>

            </div>
        `;
    });

    result.innerHTML = html;
}
async function loadProfile() {


const token = localStorage.getItem("access_token");

if (!token) {
    return;
}

try {

    const response = await fetch(
        "http://127.0.0.1:8001/profile/",
        {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }
    );

    if (!response.ok) {
        return;
    }

    const profile = await response.json();

    if (!profile) {
        return;
    }

    document.getElementById("profileGender").value =
        profile.gender || "";

    document.getElementById("profileSkinTone").value =
        profile.skin_tone || "";

    document.getElementById("profileBodyType").value =
        profile.body_type || "";

    document.getElementById("profileStyle").value =
        profile.style_preference || "";

    document.getElementById("profileColors").value =
        profile.favorite_colors || "";

} catch (error) {

    console.error("Profile loading error:", error);

}


}

async function saveProfile() {


const token = localStorage.getItem("access_token");

if (!token) {
    return;
}

const profileMessage =
    document.getElementById("profileMessage");

const profile = {

    gender:
        document.getElementById("profileGender").value,

    skin_tone:
        document.getElementById("profileSkinTone").value,

    body_type:
        document.getElementById("profileBodyType").value,

    style_preference:
        document.getElementById("profileStyle").value,

    favorite_colors:
        document.getElementById("profileColors").value

};

if (
    !profile.gender ||
    !profile.skin_tone ||
    !profile.body_type ||
    !profile.style_preference
) {

    profileMessage.innerText =
        "Please complete your profile.";

    return;
}

try {

    const response = await fetch(
        "http://127.0.0.1:8001/profile/",
        {
            method: "PUT",

            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },

            body: JSON.stringify(profile)
        }
    );

    const data = await response.json();

    if (!response.ok) {

        profileMessage.innerText =
            "Could not save profile.";

        return;
    }

    profileMessage.innerText =
        data.message || "Profile saved successfully.";

} catch (error) {

    console.error("Profile error:", error);

    profileMessage.innerText =
        "Could not connect to the API.";
}


}
function logout() {

    localStorage.removeItem("access_token");

    document.getElementById("loginSection").style.display = "block";
    document.getElementById("stylistSection").style.display = "none";
    document.getElementById("profileSection").style.display = "none";

    document.getElementById("result").innerHTML = "";

    document.getElementById("loginResult").innerText =
        "You have been logged out.";
}
