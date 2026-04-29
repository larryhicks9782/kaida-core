import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
import { getAuth, signInWithPopup, GoogleAuthProvider, signOut, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js";
import { getFunctions, httpsCallable } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-functions.js";

// [SYSTEM_WARNING]: Placeholder Configuration. Operator Larry must inject valid Firebase keys.
const firebaseConfig = {
    apiKey: "YOUR_API_KEY",
    authDomain: "YOUR_PROJECT_ID.firebaseapp.com",
    projectId: "YOUR_PROJECT_ID",
    storageBucket: "YOUR_PROJECT_ID.appspot.com",
    messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
    appId: "YOUR_APP_ID"
};

// Initialize Firebase Core
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const functions = getFunctions(app);

// DOM Mapping Directive
const loginBtn = document.getElementById('login-btn');
const logoutBtn = document.getElementById('logout-btn');
const generateBtn = document.getElementById('generate');
const appUi = document.getElementById('app-ui');
const outputDiv = document.getElementById('output');
const userEmailDiv = document.getElementById('user-email');

// Clinical Diagnostic Logger
const logDiagnostic = (msg) => {
    const timestamp = new Date().toISOString();
    console.log(`[${timestamp}] [KTRP_DIAG]: ${msg}`);
    outputDiv.textContent += `\n[${timestamp}] ${msg}`;
};

// Authentication Provider
const provider = new GoogleAuthProvider();

// Execution: Login
loginBtn.addEventListener('click', async () => {
    try {
        logDiagnostic("Initiating Google Auth Sequence...");
        const result = await signInWithPopup(auth, provider);
        logDiagnostic(`Sign-In Absolute: Identity verified as ${result.user.email}`);
    } catch (error) {
        logDiagnostic(`Sign-In Failure [ERR_${error.code}]: ${error.message}`);
    }
});

// Execution: Logout
logoutBtn.addEventListener('click', async () => {
    try {
        logDiagnostic("Purging active session...");
        await signOut(auth);
        logDiagnostic("Session purged successfully.");
    } catch (error) {
        logDiagnostic(`Sign-Out Failure [ERR_${error.code}]: ${error.message}`);
    }
});

// Execution: Generate Payload (Cloud Functions execution)
generateBtn.addEventListener('click', async () => {
    try {
        logDiagnostic("Triggering cloud function 'generate' protocol...");
        // Ensure this matches a valid exported function in your Firebase Functions
        const executeGenerate = httpsCallable(functions, 'generate'); 
        const response = await executeGenerate({ nexus_status: "ABSOLUTE" });
        logDiagnostic(`Payload Response: ${JSON.stringify(response.data)}`);
    } catch (error) {
        logDiagnostic(`Execution Failure: ${error.message}`);
    }
});

// State Reconciliation (Observer)
onAuthStateChanged(auth, (user) => {
    if (user) {
        logDiagnostic(`State Synchronized: [AUTHENTICATED] -> ${user.email}`);
        loginBtn.style.display = 'none';
        logoutBtn.style.display = 'inline-block';
        appUi.style.display = 'block';
        userEmailDiv.textContent = `[USER_ID]: ${user.email}`;
    } else {
        logDiagnostic("State Synchronized: [UNAUTHENTICATED] -> DOM collapsed to default.");
        loginBtn.style.display = 'inline-block';
        logoutBtn.style.display = 'none';
        appUi.style.display = 'none';
        userEmailDiv.textContent = '';
    }
});

logDiagnostic("Logic Core Shards initialized. Event mapping active.");