using System;
using System.Drawing;
using System.Windows.Forms;

namespace GrietasDetectApp
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        // Método que se ejecuta al hacer clic en el botón "Procesar Imagen"
        private void btnProcesar_Click(object sender, EventArgs e)
        {
            // Ruta de la imagen original (cambia esto con la ruta correcta)
            string imagePath = @"C:\Users\Erick\Desktop\imagen\1.jpg"; // Cambia esto con la ruta correcta de tu imagen

            // Cargar la imagen original
            Bitmap originalImage = new Bitmap(imagePath);
            pictureBoxOriginal.Image = originalImage;

            // Convertir a escala de grises
            Bitmap grayImage = ConvertToGrayscale(originalImage);

            // Detectar bordes
            Bitmap edgesImage = DetectEdges(grayImage);

            // Mostrar la imagen con bordes detectados en pictureBoxResultado
            pictureBoxResultado.Image = edgesImage;
        }

        // Convertir la imagen a escala de grises
        static Bitmap ConvertToGrayscale(Bitmap image)
        {
            Bitmap grayImage = new Bitmap(image.Width, image.Height);
            for (int y = 0; y < image.Height; y++)
            {
                for (int x = 0; x < image.Width; x++)
                {
                    Color pixelColor = image.GetPixel(x, y);
                    int grayValue = (int)(pixelColor.R * 0.3 + pixelColor.G * 0.59 + pixelColor.B * 0.11);
                    Color grayPixel = Color.FromArgb(grayValue, grayValue, grayValue);
                    grayImage.SetPixel(x, y, grayPixel);
                }
            }
            return grayImage;
        }

        // Detectar bordes utilizando diferencia de píxeles
        static Bitmap DetectEdges(Bitmap grayImage)
        {
            Bitmap edgeImage = new Bitmap(grayImage.Width, grayImage.Height);
            for (int y = 1; y < grayImage.Height - 1; y++)
            {
                for (int x = 1; x < grayImage.Width - 1; x++)
                {
                    int currentPixel = grayImage.GetPixel(x, y).R;
                    int leftPixel = grayImage.GetPixel(x - 1, y).R;
                    int topPixel = grayImage.GetPixel(x, y - 1).R;

                    int edgeValue = Math.Abs(currentPixel - leftPixel) + Math.Abs(currentPixel - topPixel);

                    if (edgeValue > 20) // Umbral de diferencia
                    {
                        edgeImage.SetPixel(x, y, Color.Black); // Borde
                    }
                    else
                    {
                        edgeImage.SetPixel(x, y, Color.White); // Sin borde
                    }
                }
            }
            return edgeImage;
        }

        private void btnProcesar_Click_1(object sender, EventArgs e)
        {
            // Ruta de la imagen original (cambia esto con la ruta correcta)
            string imagePath = @"C:\Users\Erick\Desktop\imagen\1.jpg"; // Cambia esto con la ruta correcta de tu imagen

            // Cargar la imagen original
            Bitmap originalImage = new Bitmap(imagePath);
            pictureBoxOriginal.Image = originalImage;

            // Convertir a escala de grises
            Bitmap grayImage = ConvertToGrayscale(originalImage);

            // Detectar bordes
            Bitmap edgesImage = DetectEdges(grayImage);

            // Mostrar la imagen con bordes detectados en pictureBoxResultado
            pictureBoxResultado.Image = edgesImage;
        }
    }
}
