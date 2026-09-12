import asyncio
import logging
from dataclasses import dataclass
from typing import List, Optional, Dict
import random
from datetime import datetime

# Configure professional logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("TradingBot")

# ==========================================
# 1. Data Structures & Domain Models
# ==========================================

@dataclass
class MarketTick:
    """Represents a single point of market data."""
    symbol: str
    price: float
    timestamp: datetime
    volume: float

@dataclass
class Order:
    """Represents a trading order."""
    symbol: str
    side: str  # 'BUY' or 'SELL'
    quantity: float
    price: Optional[float] = None # None means market order
    order_id: Optional[str] = None
    status: str = 'PENDING'

# ==========================================
# 2. Interfaces (Simulated Exchange)
# ==========================================

class MockExchange:
    """Simulates an exchange connection for paper trading."""
    
    def __init__(self):
        self.current_prices = {"BTC/USD": 50000.0, "ETH/USD": 3000.0}
        self.latency_ms = 100
        
    async def fetch_ticker(self, symbol: str) -> MarketTick:
        """Simulates fetching real-time ticker data."""
        await asyncio.sleep(self.latency_ms / 1000.0)
        # Random walk for price simulation
        change = random.uniform(-0.001, 0.001)
        self.current_prices[symbol] = self.current_prices[symbol] * (1 + change)
        
        return MarketTick(
            symbol=symbol,
            price=round(self.current_prices[symbol], 2),
            timestamp=datetime.utcnow(),
            volume=random.uniform(1, 10)
        )
        
    async def place_order(self, order: Order) -> Order:
        """Simulates order execution."""
        await asyncio.sleep(self.latency_ms / 1000.0)
        order.order_id = f"ORD_{random.randint(1000, 9999)}"
        order.status = 'FILLED'
        # In a real system, you would check balance, apply fees, handle partial fills
        return order

# ==========================================
# 3. Strategy & Alpha Generation
# ==========================================

class SimpleMovingAverageStrategy:
    """
    A basic strategy that buys when the short SMA crosses above the long SMA,
    and sells when it crosses below.
    """
    def __init__(self, short_window: int = 3, long_window: int = 5):
        self.short_window = short_window
        self.long_window = long_window
        self.price_history: Dict[str, List[float]] = {}
        
    def on_tick(self, tick: MarketTick) -> Optional[str]:
        """Processes a market tick and returns a signal ('BUY', 'SELL', or None)."""
        if tick.symbol not in self.price_history:
            self.price_history[tick.symbol] = []
            
        history = self.price_history[tick.symbol]
        history.append(tick.price)
        
        # Keep only what we need
        if len(history) > self.long_window:
            history.pop(0)
            
        if len(history) < self.long_window:
            return None # Not enough data to calculate indicators
            
        short_sma = sum(history[-self.short_window:]) / self.short_window
        long_sma = sum(history[-self.long_window:]) / self.long_window
        
        logger.debug(f"[{tick.symbol}] Short SMA: {short_sma:.2f}, Long SMA: {long_sma:.2f}")
        
        # Extremely simplified logic for demonstration
        if short_sma > long_sma * 1.0005: # Add a small threshold to avoid noise
            return 'BUY'
        elif short_sma < long_sma * 0.9995:
            return 'SELL'
            
        return None

# ==========================================
# 4. Bot Orchestrator
# ==========================================

class TradingBot:
    """Coordinates data ingestion, strategy execution, and order management."""
    def __init__(self, symbol: str, exchange: MockExchange, strategy: SimpleMovingAverageStrategy):
        self.symbol = symbol
        self.exchange = exchange
        self.strategy = strategy
        self.position = 0.0 # Current holdings
        self.is_running = False
        
    async def run(self, max_iterations: int = 10):
        """Main event loop of the trading bot."""
        self.is_running = True
        logger.info(f"Starting trading bot for {self.symbol}")
        
        for i in range(max_iterations):
            if not self.is_running:
                break
                
            try:
                # 1. Fetch Data
                tick = await self.exchange.fetch_ticker(self.symbol)
                logger.info(f"Tick received: {tick.symbol} @ ${tick.price:,.2f}")
                
                # 2. Evaluate Strategy
                signal = self.strategy.on_tick(tick)
                
                # 3. Execute Order based on Signal and Risk/Position limits
                if signal == 'BUY' and self.position <= 0:
                    logger.info(f"Generated BUY signal. Placing order.")
                    order = Order(symbol=self.symbol, side='BUY', quantity=1.0)
                    filled_order = await self.exchange.place_order(order)
                    self.position += filled_order.quantity
                    logger.info(f"Order {filled_order.order_id} FILLED. Current position: {self.position}")
                    
                elif signal == 'SELL' and self.position > 0:
                    logger.info(f"Generated SELL signal. Placing order.")
                    order = Order(symbol=self.symbol, side='SELL', quantity=1.0)
                    filled_order = await self.exchange.place_order(order)
                    self.position -= filled_order.quantity
                    logger.info(f"Order {filled_order.order_id} FILLED. Current position: {self.position}")
                    
            except Exception as e:
                logger.error(f"Error in main loop: {e}", exc_info=True)
                
            # Wait before polling next tick
            await asyncio.sleep(1)
            
        logger.info("Trading bot shut down gracefully.")


# ==========================================
# 5. Execution Entry Point
# ==========================================

async def main():
    exchange = MockExchange()
    strategy = SimpleMovingAverageStrategy(short_window=2, long_window=4)
    bot = TradingBot(symbol="BTC/USD", exchange=exchange, strategy=strategy)
    
    # Run the bot for a limited number of iterations for demonstration
    await bot.run(max_iterations=15)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot manually stopped by user.")
