from supabase import create_client, Client

url = "https://sjynjvcnopxfkxdtqfft.supabase.co"

key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNqeW5qdmNub3B4Zmt4ZHRxZmZ0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDYzMjYyODgsImV4cCI6MjA2MTkwMjI4OH0.-fF2Q7fPcsy7PGGK8JtsB7Iqi3D0mFHVBcvXlTaLBpo"

supabase: Client = create_client(url, key)

##PRUEBA DE BASE DE DATOS SUPABASE
response = supabase.table("productos").select("*").limit(5).execute()

resultado = supabase.table("productos").select("*", count="exact").execute()
print(f" Total de productos: {resultado.count}")


print("Conexión exitosa. Primeros productos:")
for producto in response.data:
    print(producto)
