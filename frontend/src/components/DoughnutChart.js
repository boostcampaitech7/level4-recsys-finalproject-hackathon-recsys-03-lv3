import React from "react";
import { Doughnut } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";

// ✅ Chart.js에 필요한 모듈 등록
ChartJS.register(ArcElement, Tooltip, Legend);

const DoughnutChart = ({ data, style = {} }) => {
  const chartData = {
    labels: ["완료된 프로젝트", "진행 중 프로젝트"],
    datasets: [
      {
        data: data, // 예: [60, 40]
        backgroundColor: ["#17B294", "#FFA500"], // ✅ 색상 설정
        borderWidth: 1,
      },
    ],
  };

  const options = {
    plugins: {
      legend: {
        display: true, // ✅ 범례 표시
        position: "bottom",
        labels: {
          padding: 30,
        },
      },
    },
  };

  return (
    <div style={{ ...style }}>
      <Doughnut data={chartData} options={options} />
    </div>
  );
};

export default DoughnutChart;
