import dotenv from "dotenv";
import express from "express";
import { logger, logEvents } from "./middleware/logger.js";
import cors from "cors";
import { corsOptions } from "./config/corsOptions.js";
import { connectDB } from "./config/dbConn.js";
import mongoose from "mongoose";
import userRoutes from "./routes/users.js";
import calendarRoutes from "./routes/calendars.js";
import eventRoutes from "./routes/events.js";
import taskRoutes from "./routes/tasks.js";
import shareRoutes from "./routes/shares.js";

dotenv.config();
connectDB();

const app = express();
app.use(logger);
app.use(cors(corsOptions));
app.use(express.json());
app.use((req, res, next) => {
  next();
});

app.use("/api/user", userRoutes);
app.use("/api/shares", shareRoutes);
app.use("/api/calendars", calendarRoutes);
app.use("/api/tasks", taskRoutes);
app.use("/api/events", eventRoutes);

mongoose.connection.once("open", () => {
  console.log("Connected to MongoDB");
  app.listen(process.env.PORT, () =>
    console.log(`Server running on port ${process.env.PORT}`)
  );
});

mongoose.connection.on("error", (err) => {
  console.log(err);
  logEvents(
    `${err.no}: ${err.code}\t${err.syscall}\t${err.hostname}`,
    "mongoErrLog.log"
  );
});
