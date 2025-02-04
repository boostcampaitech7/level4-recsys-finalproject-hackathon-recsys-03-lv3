import React from "react";
import { Box, Slider, Typography, Rating } from "@mui/material";

const RatingSlider = ({ label, value = 3.0, onChange }) => {
  return (
    <Box sx={{ display: "flex", alignItems: "center", width: "100%", my: 2 }}>
      {/* 슬라이더 & 별점 영역 */}
      <Box
        sx={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <Typography variant="body1">{label}</Typography>
        <Rating
          value={value}
          precision={0.1}
          onChange={(_, newValue) => onChange(newValue)}
        />
        <Slider
          value={value}
          min={0.0}
          max={5.0}
          step={0.1}
          onChange={(_, newValue) => onChange(newValue)}
          valueLabelDisplay="auto"
          sx={{ width: "80%" }}
        />
      </Box>

      {/* 점수 표시 영역 */}
      <Typography variant="h6" sx={{ width: "50px", textAlign: "center" }}>
        {value.toFixed(1)}
      </Typography>
    </Box>
  );
};

export default RatingSlider;
