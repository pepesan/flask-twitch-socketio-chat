import asyncio

async def tarea1():
    print("Tarea 1 iniciada")
    await asyncio.sleep(2)  # Simular una tarea que toma 2 segundos
    print("Tarea 1 completada")

async def tarea2():
    print("Tarea 2 iniciada")
    await asyncio.sleep(1)  # Simular una tarea que toma 1 segundo
    print("Tarea 2 completada")

async def main():
    tarea1_coro = tarea1()
    tarea2_coro = tarea2()

    await asyncio.gather(tarea1_coro, tarea2_coro)

asyncio.run(main())
