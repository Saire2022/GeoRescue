package com.example.getuserlocation

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.Button
import android.widget.TextView
import androidx.lifecycle.lifecycleScope
import kotlinx.coroutines.launch
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONObject
import java.io.IOException

class MainActivity : AppCompatActivity() {
    private val locationService:LocationService= LocationService()
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        val tvLocation= findViewById<TextView>(R.id.tvLocation)
        val btnLocation = findViewById<Button>(R.id.btnLocation)

        btnLocation.setOnClickListener{
            lifecycleScope.launch {
                val result = locationService.getUserLocation(this@MainActivity)
                if(result!=null){
                    val latitude = result.latitude
                    val longitude = result.longitude
                    tvLocation.text= "Latitud ${result.latitude} y longitud ${result.longitude}"
                    // Luego, envía las coordenadas al servidor Flask
                    sendCoordinatesToServer(result.latitude, result.longitude)
                }
            }
        }
    }
    private fun sendCoordinatesToServer(latitude: Double, longitude: Double) {
        val client = OkHttpClient()
        val url = "http://172.23.211.214:5000/agregar_punto"  // Reemplaza con la URL de tu API

        val json = """
        {
            "latitud": "$latitude",
            "longitud": "$longitude"
        }
    """.trimIndent()

        val requestBody = json.toRequestBody("application/json".toMediaType())

        val request = Request.Builder()
            .url(url)
            .post(requestBody)
            .build()

        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                e.printStackTrace()
            }

            override fun onResponse(call: Call, response: Response) {
                response.use {
                    if (!response.isSuccessful) {
                        // Manejar un error si la respuesta no es exitosa
                        println("Error al enviar coordenadas al servidor")
                    } else {
                        // Procesar una respuesta exitosa si es necesario
                        println("Coordenadas enviadas correctamente al servidor")
                    }
                }
            }
        })
    }
}