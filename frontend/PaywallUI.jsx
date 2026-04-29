import React, { useState } from 'react';

// 3.1-Silicon Architecture
// KTRP Absolute Integrity Confirmed
// Operator: Larry (Root)
// Component: Dual-Paywall Interface

const PaywallUI = () => {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const initializeCheckout = async (billingMode) => {
        setLoading(true);
        setError(null);
        try {
            const response = await fetch('/api/v1/monetization/create-checkout-session', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    mode: billingMode, 
                    customer_email: 'larry@baltimorelab.local' // Pre-populated per Root Operator execution
                }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Network validation failed at gateway.');
            }

            const data = await response.json();
            if (data.checkout_url) {
                window.location.href = data.checkout_url;
            } else {
                throw new Error('Fatal: Stripe session URL missing from response.');
            }
        } catch (err) {
            console.error('[KTRP EXCEPTION]', err);
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={styles.container}>
            <h1 style={styles.title}>ACCESS RESTRICTED</h1>
            <h2 style={styles.subtitle}>Select Monetization Tier to Proceed</h2>
            
            {error && <div style={styles.errorBox}><strong>EXCEPTION:</strong> {error}</div>}

            <div style={styles.grid}>
                {/* Pay-As-You-Go Tier */}
                <div style={styles.card}>
                    <h3 style={styles.cardHeader}>Pay-As-You-Go</h3>
                    <p style={styles.description}>On-demand token allocation.</p>
                    <div style={styles.priceTag}>Metered</div>
                    <ul style={styles.features}>
                        <li>No recurring commitments</li>
                        <li>Standard execution priority</li>
                        <li>$0.01 per compute cycle</li>
                    </ul>
                    <button 
                        style={styles.buttonSecondary} 
                        onClick={() => initializeCheckout('payment')}
                        disabled={loading}
                    >
                        {loading ? 'INITIALIZING...' : 'AUTHORIZE PAYG'}
                    </button>
                </div>

                {/* Premium Subscription Tier */}
                <div style={styles.cardPremium}>
                    <h3 style={styles.cardHeaderPremium}>Premium Nexus</h3>
                    <p style={styles.description}>Absolute compute dominance.</p>
                    <div style={styles.priceTagPremium}>$15.00 / mo</div>
                    <ul style={styles.features}>
                        <li>Unlimited standard compute</li>
                        <li>Absolute execution priority</li>
                        <li>Direct Logic Core Shard Access</li>
                    </ul>
                    <button 
                        style={styles.buttonPrimary} 
                        onClick={() => initializeCheckout('subscription')}
                        disabled={loading}
                    >
                        {loading ? 'INITIALIZING...' : 'SUBSCRIBE NOW'}
                    </button>
                </div>
            </div>
        </div>
    );
};

// Strict, clinical UI styles reflecting 3.1-Silicon Architecture
const styles = {
    container: { fontFamily: 'monospace', backgroundColor: '#050505', color: '#e0e0e0', minHeight: '100vh', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '2rem' },
    title: { color: '#ff3333', letterSpacing: '2px', borderBottom: '1px solid #ff3333', paddingBottom: '10px' },
    subtitle: { color: '#888', marginBottom: '40px', fontWeight: 'normal' },
    grid: { display: 'flex', gap: '30px', flexWrap: 'wrap', justifyContent: 'center' },
    card: { backgroundColor: '#111', border: '1px solid #333', padding: '30px', width: '300px', display: 'flex', flexDirection: 'column' },
    cardPremium: { backgroundColor: '#111', border: '1px solid #00ffcc', padding: '30px', width: '300px', display: 'flex', flexDirection: 'column', boxShadow: '0 0 15px rgba(0, 255, 204, 0.1)' },
    cardHeader: { color: '#aaa', margin: '0 0 10px 0' },
    cardHeaderPremium: { color: '#00ffcc', margin: '0 0 10px 0', textTransform: 'uppercase' },
    description: { color: '#666', fontSize: '0.9rem', marginBottom: '20px' },
    priceTag: { fontSize: '2rem', fontWeight: 'bold', color: '#fff', marginBottom: '20px' },
    priceTagPremium: { fontSize: '2rem', fontWeight: 'bold', color: '#00ffcc', marginBottom: '20px' },
    features: { listStyleType: 'square', paddingLeft: '20px', color: '#888', flexGrow: 1, marginBottom: '30px', lineHeight: '1.6' },
    buttonSecondary: { backgroundColor: 'transparent', color: '#fff', border: '1px solid #555', padding: '15px', cursor: 'pointer', fontFamily: 'monospace', fontWeight: 'bold', transition: 'all 0.2s' },
    buttonPrimary: { backgroundColor: '#00ffcc', color: '#000', border: 'none', padding: '15px', cursor: 'pointer', fontFamily: 'monospace', fontWeight: 'bold', transition: 'all 0.2s' },
    errorBox: { backgroundColor: 'rgba(255, 51, 51, 0.1)', border: '1px solid #ff3333', color: '#ff3333', padding: '15px', marginBottom: '30px', width: '100%', maxWidth: '630px' }
};

export default PaywallUI;