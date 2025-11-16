
import React, {useState} from 'react';

function App(){
  const [exchange, setExchange] = useState('binance');
  const [symbol, setSymbol] = useState('BTC/USDT');
  const [data, setData] = useState(null);

  async function fetchTicker(){
    const res = await fetch(`/ticker?exchange=${exchange}&symbol=${encodeURIComponent(symbol)}`, {headers:{'X-API-KEY':'demo-key-123'}});
    const j = await res.json();
    setData(j);
  }

  return (
    <div style={{padding:20}}>
      <h2>MCP Demo</h2>
      <div>
        <input value={exchange} onChange={e=>setExchange(e.target.value)} />
        <input value={symbol} onChange={e=>setSymbol(e.target.value)} />
        <button onClick={fetchTicker}>Fetch</button>
      </div>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  )
}

export default App;
