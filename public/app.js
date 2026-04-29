import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-app.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-auth.js";
import { getFunctions, httpsCallable } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-functions.js";

const firebaseConfig = {
  apiKey: "KEY_REDACTED",
  authDomain: "titan-lab-9782.firebaseapp.com",
  projectId: "titan-lab-9782",
  storageBucket: "titan-lab-9782.firebasestorage.app",
  messagingSenderId: "626877214205",
  appId: "1:626877214205:web:1bdc1e895923305e7d3d94"
};

// Initialize Firebase Nexus Services
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const functions = getFunctions(app);

// Initialize DOM interface instances
const generateButton = document.getElementById('generateButton');
const outputBox = document.getElementById('outputBox');

if (generateButton && outputBox) {
    generateButton.addEventListener('click', async () => {
        outputBox.innerHTML = "<p>Processing request via Kaida Architecture Node...</p>";
        
        try {
            const generateArchitecture = httpsCallable(functions, 'generate_architecture');
            const result = await generateArchitecture({ timestamp: Date.now() });
            
            outputBox.innerHTML = `<p>Status: ARCHITECTURE_GENERATED.</p><pre>${JSON.stringify(result.data, null, 2)}</pre>`;
        } catch (error) {
            console.error("[KAIDA_NEXUS_ERROR]:", error);
            
            // Trap for Dual-Paywall response
            if (error.message === "PAYWALL_ACTIVE" || error.code === "functions/permission-denied" || (error.details && error.details.status === "PAYWALL_ACTIVE")) {
                outputBox.innerHTML = `
                    <div class="paywall-container" style="text-align: center; border: 1px solid #cc0000; padding: 20px; background: #1a0000; color: #ff3333; font-family: monospace;">
                        <h3>[ACCESS DENIED: PAYWALL_ACTIVE]</h3>
                        <p>Insufficient computational clearance. Select a monetization tier to proceed:</p>
                        <br/>
                        <a href="/checkout/payg" class="paywall-btn" style="display: inline-block; padding: 12px 24px; margin: 10px; background: #333; color: #fff; text-decoration: none; border: 1px solid #555; border-radius: 4px; font-weight: bold;">PAY AS YOU GO (100 Tokens)</a>
                        <a href="/checkout/pro" class="paywall-btn" style="display: inline-block; padding: 12px 24px; margin: 10px; background: #0055ff; color: #fff; text-decoration: none; border: 1px solid #0044cc; border-radius: 4px; font-weight: bold;">UPGRADE TO PRO ($15/mo)</a>
                    </div>
                `;
            } else {
                outputBox.innerHTML = `<p style="color: red;">[SYSTEM_ERROR]: ${error.message}</p>`;
            }
        }
    });
} else {
    console.warn("[KAIDA_WARNING]: Required DOM elements 'generateButton' or 'outputBox' not found in document. Verify index.html rendering sequence.");
}
