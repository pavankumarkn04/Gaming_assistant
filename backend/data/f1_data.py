F1_DATA = [
    # Teams
    {
        "id": "f1_team_redbull",
        "game": "f1",
        "category": "team",
        "title": "Red Bull Racing - Team Guide 2024",
        "content": """Red Bull Racing (Oracle Red Bull Racing) - 2024 season overview.
        Car: RB20.
        Drivers: Max Verstappen (#1), Sergio Perez (#11).
        Engine: Honda RBPT (Honda-derived power unit).

        Car strengths: Exceptional downforce efficiency, superb high-speed cornering, very low drag.
        Car weaknesses: Can struggle in wet conditions, Perez underperforming vs Verstappen.

        Base: Milton Keynes, UK.
        Team Principal: Christian Horner.

        2024 form: Dominant early season, Verstappen winning most races, but McLaren and Ferrari closing gap significantly mid-season.
        Tyre management: Red Bull historically excellent at tyre conservation.
        Strategy style: Aggressive one-stop strategies, undercut preference.

        Constructor championship standing: Strong title contenders every year since 2022.
        Key strength in F1 game (EA Sports F1): Highest top speed package, best cornering stability."""
    },
    {
        "id": "f1_team_mclaren",
        "game": "f1",
        "category": "team",
        "title": "McLaren F1 Team - Team Guide 2024",
        "content": """McLaren F1 Team - 2024 season overview.
        Car: MCL38.
        Drivers: Lando Norris (#4), Oscar Piastri (#81).
        Engine: Mercedes.

        Car strengths: Excellent tyre management, strong mid-high speed corners, best in class race pace late 2024.
        Car weaknesses: Early season struggled with quali pace vs Red Bull.

        Base: Woking, UK.
        Team Principal: Andrea Stella.

        2024 form: Massive step forward, won multiple races in second half of season, Norris challenging Verstappen for WDC.
        Strategy style: Flexible two-stop when needed, innovative strategy calls (Budapest 2024 double stack).
        Key battles: Norris vs Verstappen for championship, Piastri emerging as top-tier talent.

        In F1 game: Best balanced car, excellent for wet weather setups, strong tyre wear simulations."""
    },
    {
        "id": "f1_team_ferrari",
        "game": "f1",
        "category": "team",
        "title": "Ferrari - Team Guide 2024",
        "content": """Scuderia Ferrari - 2024 season overview.
        Car: SF-24.
        Drivers: Charles Leclerc (#16), Carlos Sainz (#55).
        Engine: Ferrari.

        Car strengths: Strong in qualifying (low fuel pace), excellent traction out of slow corners.
        Car weaknesses: Strategic errors under pressure, tyre deg on hot tracks.

        Base: Maranello, Italy.
        Team Principal: Frederic Vasseur.

        2024 form: Strong quali performances, race pace inconsistent, Leclerc won Monaco GP.
        Strategy weakness: Historically poor strategic decisions under pressure (Abu Dhabi, Monza).
        Sainz departure: Carlos Sainz leaving for Williams in 2025, Hamilton joining Ferrari.

        In F1 game: Best for slow-speed tracks and street circuits (Monaco, Singapore), requires tyre management focus in career mode."""
    },
    # Circuits
    {
        "id": "f1_circuit_monaco",
        "game": "f1",
        "category": "circuit",
        "title": "Monaco Grand Prix Circuit Guide",
        "content": """Circuit de Monaco - Iconic street circuit.
        Length: 3.337 km. Laps: 78.
        Location: Monte Carlo, Monaco.
        Circuit type: Street circuit.

        Key corners:
        - Sainte Devote (T1): Hard braking right-hander, heavy traffic start.
        - Massenet: Fast left through the Casino complex.
        - Casino Square: Slow chicane, tricky on bumps.
        - Mirabeau: Steep downhill hairpin.
        - Fairmont Hairpin (Loews): Tightest corner in F1, 42 km/h.
        - Portier: Rhythm section leading to tunnel.
        - Tunnel: Full throttle, blind exit, speed trap section.
        - Chicane (nouvelle): Hard braking chicane after tunnel.
        - Rascasse: Hairpin before pit straight.
        - Antony Noghes (T19): Final corner onto pit straight.

        F1 game setup tips:
        - Maximum downforce, street circuit specific tyres.
        - Short gearing for low top speed but high acceleration.
        - Suspension stiff to handle bumps.
        - Braking balance slightly forward.

        Overtaking: Nearly impossible. Qualifying position is crucial. Race strategy often locked in.
        Weather impact: Rain causes huge chaos, safety car almost guaranteed."""
    },
    {
        "id": "f1_circuit_monza",
        "game": "f1",
        "category": "circuit",
        "title": "Monza Circuit Guide - Temple of Speed",
        "content": """Autodromo Nazionale Monza - Fastest circuit in F1.
        Length: 5.793 km. Laps: 53.
        Location: Monza, Italy.

        Key corners:
        - Prima Variante (T1-T2): Heavy braking chicane at 345km/h.
        - Seconda Variante: Second chicane, traction critical.
        - Lesmo 1 & 2: Fast sweeping right-handers through the forest.
        - Parabolica (T11-T12): Long final corner, crucial for straight-line speed.
        - Ascari Chicane: S-bend sequence.

        F1 game setup tips:
        - Minimum downforce for maximum straight-line speed.
        - Soft suspension for flat track.
        - Long gear ratios.
        - Late braking is rewarded here, strong brake bias.

        DRS zones: Two long DRS zones, huge slipstream opportunities.
        Strategy: Often two-stop on mediums/hards. Tyre deg is low. Undercut very effective.
        Overtaking: One of the best circuits for racing, many opportunities at T1 and Parabolica."""
    },
    {
        "id": "f1_circuit_spa",
        "game": "f1",
        "category": "circuit",
        "title": "Spa-Francorchamps Circuit Guide",
        "content": """Circuit de Spa-Francorchamps - Most legendary racing circuit.
        Length: 7.004 km. Laps: 44.
        Location: Spa, Belgium.

        Key corners:
        - La Source (T1): Tight right hairpin, heavy traffic on lap 1.
        - Eau Rouge/Raidillon: Iconic uphill esses, full throttle in modern F1. Most famous section.
        - Kemmel Straight: Long DRS zone, main overtaking area.
        - Les Combes: Chicane at top, hard braking.
        - Pouhon: Fast double-left, high G-force.
        - Blanchimont: Near full-throttle left, leads to Bus Stop.
        - Bus Stop (T19): Final chicane, important for final lap positions.

        F1 game setup tips:
        - Medium downforce compromise (need speed on Kemmel, grip at Pouhon).
        - Strong aero balance for Eau Rouge.
        - High-speed suspension tuning.

        Weather: Unpredictable. Famous for rain at one end, dry at other. Intermediate tyres essential.
        Strategy: Variable depending on weather. Safety car probability high. Two-stop typical.
        Career mode tips: Great circuit to master early, awards high points in challenge modes."""
    },
    # Race strategies
    {
        "id": "f1_strategy_tyre",
        "game": "f1",
        "category": "strategy",
        "title": "F1 Tyre Strategy Guide",
        "content": """Understanding F1 tyre strategy is crucial for race success.

        Tyre compounds:
        - Soft (Red): Fastest, least durable. Good for qualifying and sprint first stints.
        - Medium (Yellow): Balanced performance and durability. Most versatile race tyre.
        - Hard (White): Slowest but very durable. Can go very long stints.
        - Intermediate (Green): Wet but not fully wet. Light rain, damp track.
        - Full Wet (Blue): Heavy rain. Very slow in dry, essential in downpour.

        Strategy types:
        - One-stop: Start on Soft/Medium, switch to Hard for long final stint.
        - Two-stop: More aggressive, fresher tyres throughout, loses time in pit lane.
        - Undercut: Pit early before rival, gain track position with fresh tyre pace.
        - Overcut: Stay out longer than rival, gain position by not pitting (works if tyre holds).

        In-game tips (EA Sports F1):
        - Tyre age matters: 0-10 laps is peak, 10-25 degrading, 25+ critical.
        - Push when warm, conserve when leading.
        - Rain switch timing: Pit for Inters when track is 'damp' (80% wet display).
        - Use MFD (Multi Function Display) to monitor tyre temps — keep in green zone."""
    },
    # Drivers
    {
        "id": "f1_driver_verstappen",
        "game": "f1",
        "category": "driver",
        "title": "Max Verstappen - Driver Profile",
        "content": """Max Verstappen - 3x World Champion (2021, 2022, 2023).
        Team: Red Bull Racing. Number: #1.
        Nationality: Dutch/Belgian.

        Strengths: Aggressive braking, exceptional wet weather driving, tyre management, qualifying pace.
        Weaknesses: Sometimes controversial under pressure (early career), can be aggressive in wheel-to-wheel.

        Driving style: Very late braking, car on edge of control, maximizes every tenth.
        Career stats: 50+ race wins, most wins in a single season (2023 - 19 wins).
        Championships: 2021 (dramatic final lap Abu Dhabi), 2022 (dominant), 2023 (historic).

        In F1 game career mode:
        - Verstappen has near-max ratings: Racecraft 98, Awareness 97, Pace 99, Experience 95.
        - Best AI opponent on highest difficulty.
        - In My Team mode: Most expensive driver hire.

        Notable races: 2021 Dutch GP comeback, 2022 Brazil overtake on Leclerc, 2023 total domination."""
    },
    {
        "id": "f1_driver_norris",
        "game": "f1",
        "category": "driver",
        "title": "Lando Norris - Driver Profile",
        "content": """Lando Norris - McLaren's lead driver, first F1 win 2024 Miami GP.
        Team: McLaren. Number: #4.
        Nationality: British.

        Strengths: Exceptional one-lap qualifying pace, smooth tyre management, consistent race performer.
        Weaknesses: Earlier career lost points from incidents under pressure (2021 Sochi rain incident).

        Driving style: Smooth inputs, great at preserving tyres, very technically precise.
        2024 season: Emerged as genuine title challenger to Verstappen.
        First win: 2024 Miami Grand Prix.

        In F1 game:
        - Ratings: Racecraft 93, Awareness 90, Pace 95, Experience 78.
        - Great for players who prefer technical, consistent driving over raw aggression.
        - Strong at tire preservation circuits (Monza, Suzuka in game).

        Fun facts: Popular streamer/content creator. Major gaming audience. Perfect STAN ambassador."""
    },
    # Car setups
    {
        "id": "f1_setup_guide",
        "game": "f1",
        "category": "car_setup",
        "title": "F1 Game Car Setup Guide - Complete Breakdown",
        "content": """Complete car setup guide for EA Sports F1 games.

        Aerodynamics:
        - Front Wing: Higher = more front grip, more drag. Lower = less grip, less drag.
        - Rear Wing: Same principle. High downforce for slow circuits (Monaco), low for fast (Monza).
        - Balance: Front slightly higher than rear for oversteer resistance.

        Transmission:
        - On Throttle Diff: Lower (50%) = more oversteer on exit, faster but risky. Higher = understeer but stable.
        - Off Throttle Diff: Lower = more rotation under braking, higher = stability.

        Suspension Geometry:
        - Camber: Front -2.5 to -3.5, Rear -1.0 to -2.0. More negative = more grip but more wear.
        - Toe: Front -0.05 to -0.15, Rear 0.20 to 0.40. More rear toe = stability.

        Suspension:
        - Higher ride height = less drag, safer floor hits. Lower = more downforce.
        - Stiff suspension = better aero, but bouncy on bumps (bad for Monaco).

        Brakes:
        - Brake Pressure: 100% for aggressive braking. Reduce to 80-90% if locking up.
        - Brake Bias: Higher = more front braking. 55-58% standard.

        Tyres:
        - Pressure: Lower = more grip, more heat, more wear. Higher = less grip, cooler.
        - Front 22.0-23.5 PSI, Rear 20.0-21.0 PSI typical.

        Quick setup presets by circuit type:
        - High downforce (Monaco, Hungary): Front 9/11, Rear 9/11, Stiff suspension.
        - Low downforce (Monza, Baku): Front 1/3, Rear 1/3, Soft suspension.
        - Balanced (Silverstone, Barcelona): Front 5/7, Rear 5/7, Medium settings."""
    }
]
