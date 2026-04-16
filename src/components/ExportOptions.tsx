import React, { useRef } from 'react';
import html2canvas from 'html2canvas';
import jsPDF from 'jspdf';
import useCardStore from '../store';

const ExportOptions: React.FC = () => {
  const { exportFormat, setExportFormat } = useCardStore();
  const cardRef = useRef<HTMLDivElement>(null);

  const handleExportFormatChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setExportFormat(e.target.value);
  };

  const handleExport = async () => {
    const cardElement = document.querySelector('[data-card-preview]') as HTMLElement;
    if (!cardElement) return;

    try {
      const canvas = await html2canvas(cardElement, {
        scale: 2,
        useCORS: true,
        logging: false,
      });

      if (exportFormat === 'pdf') {
        const pdf = new jsPDF('portrait', 'mm', 'a4');
        const imgData = canvas.toDataURL('image/png');
        const imgWidth = 210;
        const imgHeight = (canvas.height * imgWidth) / canvas.width;
        pdf.addImage(imgData, 'PNG', 0, 0, imgWidth, imgHeight);
        pdf.save('business-card.pdf');
      } else {
        const link = document.createElement('a');
        link.download = `business-card.${exportFormat}`;
        link.href = canvas.toDataURL(`image/${exportFormat}`);
        link.click();
      }
    } catch (error) {
      console.error('导出失败:', error);
    }
  };

  return (
    <div className="p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-6 text-gray-800">导出选项</h2>
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">导出格式</label>
          <select
            value={exportFormat}
            onChange={handleExportFormatChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="png">PNG</option>
            <option value="jpg">JPG</option>
            <option value="pdf">PDF</option>
          </select>
        </div>
        <button
          onClick={handleExport}
          className="w-full py-3 px-4 bg-blue-600 text-white font-bold rounded-md hover:bg-blue-700 transition-colors duration-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
        >
          导出卡片
        </button>
        <p className="text-sm text-gray-500">
          点击导出按钮，将根据选择的格式下载卡片
        </p>
      </div>
    </div>
  );
};

export default ExportOptions;