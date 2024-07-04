# Utilizar la imagen oficial de Node.js basada en Alpine 3.14 como imagen base
FROM node:16-alpine3.14

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar package.json y package-lock.json al directorio de trabajo
COPY package.json package-lock.json ./

# Instalar las dependencias del proyecto
RUN npm install

# Copiar el resto del código de la aplicación al directorio de trabajo
COPY . .

# Construir la aplicación para producción
RUN npm run build

# Exponer el puerto en el que la aplicación se ejecutará
EXPOSE 5173

# Comando para ejecutar la aplicación
CMD ["npm", "run", "dev", "--", "--port", "5173"]
