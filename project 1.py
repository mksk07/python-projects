import matplotlib.pyplot as plt
import fastf1.plotting
fastf1.plotting.setup_mpl(mpl_timedelta_support=True,clor_scheme='fastf1')
session=fastf1.get_session(2025, 'las vegas', 'Q')
session.load()
Nor_lap=session.laps.pick_drivers('NOR').pick_fastest()
ver_lap=session.laps.pick_drivers('VER').pick_fastest()
Nor_tel=Nor_lap.get_car_data().add_distance()
ver_tel=ver_lap.get_car_data().add_distance()

mer_color = fastf1.plotting.get_team_color(Nor_lap['Team'], session=session)
fer_color = fastf1.plotting.get_team_color(ver_lap['Team'], session=session)

fig, ax = plt.subplots()
ax.plot(Nor_tel['Distance'], Nor_tel['Speed'], color=mer_color, label='NOR')
ax.plot(ver_tel['Distance'], ver_tel['Speed'], color=fer_color, label='VER')

ax.set_xlabel('Distance in m')
ax.set_ylabel('Speed in km/h')

ax.legend()
plt.suptitle(f"Fastest Lap Comparison \n "
             f"{session.event['EventName']} {session.event.year} Qualifying")

plt.show()