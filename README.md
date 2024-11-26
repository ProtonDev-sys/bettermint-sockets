
# Bettermint Websockets

Welcome to the Bettermint Websockets! This provides access to a variety of chess engines via a single URL or allows you to host the service locally using Docker.

## Websocket URL

**Primary URL:** `wss://ProtonnDev-engine.hf.space/enginestuff`

All engines can be accessed using this single endpoint. Select the engine by appending its specific identifier to the URL (details below).

## Available Engines and Configurations

### Stockfish Engines

Access multiple versions of Stockfish by specifying the desired version in the URL.

**Usage:**

```
wss://ProtonnDev-engine.hf.space/stockfish-{version}
```

**Available Versions:**

- Stockfish 1
- Stockfish 2
- Stockfish 3
- Stockfish 5
- Stockfish 6
- Stockfish 7
- Stockfish 8
- Stockfish 9
- Stockfish 10
- Stockfish 11
- Stockfish 12
- Stockfish 13
- Stockfish 14
- Stockfish 16

**Example:**

```
wss://ProtonnDev-engine.hf.space/stockfish-11
```

### Maia Bot (Neural Network Chess Engine)

Maia Bot is designed to play human-like moves at different Elo ratings.

**Usage:**

```
wss://ProtonnDev-engine.hf.space/maia-{elo}
```

**Available Elo Ratings:**

- **maia-1100** (1100 Elo)
- **maia-1200** (1200 Elo)
- *...increments by 100...*
- **maia-1900** (1900 Elo)

**Example:**

```
wss://ProtonnDev-engine.hf.space/maia-1500
```

**Note:** Do not set the depth higher than 7 (recommended depth is 5-6) to maintain reasonable response times.

### Rodent III Engine

Rodent III is a versatile engine with various personalities, including emulations of famous chess players and fun styles.

**Default Usage:**

```
wss://ProtonnDev-engine.hf.space/rodent3-default
```

#### Personalities

You can select a personality by appending it to the URL.

**Usage:**

```
wss://ProtonnDev-engine.hf.space/rodent3-{personality}
```

**Available Personalities:**

- **anand**: Fast player, slight preference for attack, cares for pawn structure.
- **anderssen**
- **botvinnik**: Balanced, cares for pawn structure, somewhat willing to accept doubled pawns.
- **fischer**: Attacking, contemptuous, raised mobility for both sides.
- **larsen**: Tricky player, follows Nimzowitsch principles, plays varied and unusual openings, may sacrifice even if king attacks aren't the main focus.
- **marshall**: Very high attack and mobility, sacrificial, favors knights.
- **nimzowitsch**
- **petrosian**: Defensive, prefers closed positions, likes sacrificing exchange.
- **reti**: Disregards classical piece placement, solid pawn structure.
- **rubinstein**: Classical player, marginally prefers defense, decreased mobility, favors rook play, steers towards endgame.
- **spassky**: Defensive player who likes grabbing space and cares for pawn structure.
- **steinitz**: Defensive, accepts cramped positions and sacrifices, solid with pawns.
- **tarrasch**: Mobility-focused, emphasizes bishops, likes open games.

**Fun Personalities:**

- **drunk**: Huge random factor in evaluation.
- **henny**
- **kinghunter**: Mad attacker.
- **remy**
- **tortoise**: Slow defensive player who likes blocked positions.

**Examples:**

```
wss://ProtonnDev-engine.hf.space/rodent3-fischer
wss://ProtonnDev-engine.hf.space/rodent3-drunk
```

### Patricia Engine

Patricia is one of the most aggressive chess engines ever created, designed to play attacking and stylish chess.

**Usage:**

```
wss://ProtonnDev-engine.hf.space/patricia-{elo}
```

**Elo Range:** 1100 to 3200

**Examples:**

```
wss://ProtonnDev-engine.hf.space/patricia-1234
wss://ProtonnDev-engine.hf.space/patricia-2250
```

## Hosting Locally

If you want to host the service locally, follow these steps:

1. **Download Docker**: [Docker Desktop](https://www.docker.com/products/docker-desktop/).
2. **Install Docker**: Follow the standard installation process for your system. Ensure Docker is running.
3. **Download the ZIP**: Obtain the ZIP file from the [GitHub Releases](https://github.com/ProtonDev-sys/bettermint-sockets/releases).
4. **Extract and Run**:
   - Extract the ZIP file.
   - Run the `run.bat` file to install and start the Docker container.
5. **Set Your API**:
   - Use the local URL: `ws://127.0.0.1:7860/ENGINE`.
   - Replace `ENGINE` with the specific engine name from the examples above.

