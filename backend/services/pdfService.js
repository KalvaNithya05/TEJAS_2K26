const PDFDocument = require('pdfkit');
const fs = require('fs');
const path = require('path');

exports.generateReport = (data, res) => {
    const doc = new PDFDocument({ margin: 50 });

    // Set response headers
    res.setHeader('Content-Type', 'application/pdf');
    res.setHeader('Content-Disposition', 'attachment; filename=mitti-mitra-report.pdf');

    doc.pipe(res);

    // 1. Title & Header
    doc.fontSize(26).fillColor('#2E7D32').text('MITTI MITRA', { align: 'center' });
    doc.fontSize(18).fillColor('#4caf50').text('Crop & Fertilizer Recommendation Report', { align: 'center' });
    doc.fontSize(10).fillColor('#666666').text(`Generated: ${new Date().toLocaleString()}`, { align: 'center' });
    doc.moveDown(2);

    // 2. Soil Analysis Summary
    doc.fontSize(16).fillColor('#000000').text('Soil Analysis Summary', { underline: true });
    doc.moveDown(0.5);
    doc.fontSize(11);
    doc.text(`Nitrogen (N): ${data.used_params.N} mg/kg`);
    doc.text(`Phosphorus (P): ${data.used_params.P} mg/kg`);
    doc.text(`Potassium (K): ${data.used_params.K} mg/kg`);
    doc.text(`Soil pH: ${data.used_params.ph}`);
    doc.text(`Temperature: ${data.used_params.temperature}°C`);
    doc.text(`Humidity: ${data.used_params.humidity}%`);
    if (data.used_params.moisture) {
        doc.text(`Soil Moisture: ${data.used_params.moisture}%`);
    }
    if (data.used_params.soil_type) {
        doc.text(`Soil Type: ${data.used_params.soil_type}`);
    }
    doc.moveDown(2);

    // 3. Recommended Crops
    doc.fontSize(16).fillColor('#000000').text('Recommended Crops', { underline: true });
    doc.moveDown(0.5);

    if (data.crops && data.crops.length > 0) {
        data.crops.forEach((crop, index) => {
            const isBest = index === 0;
            const color = isBest ? '#2E7D32' : '#000000';

            doc.fontSize(14).fillColor(color).text(
                `${index + 1}. ${crop.crop.toUpperCase()}`,
                { continued: true }
            );
            doc.fontSize(11).fillColor('#666666').text(
                ` - ${(crop.confidence * 100).toFixed(1)}% confidence`,
                { continued: false }
            );

            if (isBest) {
                doc.fontSize(10).fillColor('#FF9800').text('   ★ Top Recommendation', { indent: 20 });
            }

            doc.moveDown(0.8);
        });
    } else {
        doc.fontSize(11).fillColor('#666666').text('No crop recommendations available.');
    }

    doc.moveDown(2);

    // 4. Fertilizer Recommendation (NEW SECTION)
    doc.fontSize(16).fillColor('#000000').text('Fertilizer Recommendation', { underline: true });
    doc.moveDown(0.5);

    if (data.fertilizer_recommendation) {
        const fert = data.fertilizer_recommendation;

        // Fertilizer name - prominent
        doc.fontSize(14).fillColor('#2E7D32').text('Recommended Fertilizer:', { continued: false });
        doc.fontSize(18).fillColor('#1B5E20').text(fert.fertilizer, { indent: 20 });
        doc.moveDown(0.3);

        // Confidence
        doc.fontSize(11).fillColor('#666666').text(
            `Confidence: ${(fert.confidence * 100).toFixed(1)}%`,
            { indent: 20 }
        );
        doc.moveDown(1);

        // Reasoning
        if (fert.reasoning && fert.reasoning.length > 0) {
            doc.fontSize(13).fillColor('#000000').text('Why this fertilizer?');
            doc.moveDown(0.3);
            doc.fontSize(10).fillColor('#555555');

            fert.reasoning.forEach((reason, index) => {
                doc.text(`• ${reason}`, { indent: 20 });
                doc.moveDown(0.3);
            });
        }
    } else {
        doc.fontSize(11).fillColor('#666666').text('No fertilizer recommendation available.');
    }

    doc.moveDown(2);

    // 5. Application Guidelines
    doc.addPage();
    doc.fontSize(16).fillColor('#000000').text('Application Guidelines', { underline: true });
    doc.moveDown(0.5);
    doc.fontSize(11).fillColor('#555555');
    doc.text('1. Apply fertilizer during early morning or late evening to minimize nutrient loss.');
    doc.text('2. Ensure soil has adequate moisture before fertilizer application.');
    doc.text('3. Follow recommended dosage based on crop stage and field size.');
    doc.text('4. Monitor crop response and adjust application as needed.');
    doc.text('5. Maintain proper spacing and avoid over-application.');
    doc.moveDown(2);

    // 6. Important Notes
    doc.fontSize(14).fillColor('#FF6F00').text('Important Notes:', { underline: true });
    doc.moveDown(0.5);
    doc.fontSize(10).fillColor('#555555');
    doc.text('• This recommendation is based on current soil analysis and AI predictions.');
    doc.text('• Soil conditions may vary across different parts of the field.');
    doc.text('• Consider conducting soil tests periodically for best results.');
    doc.text('• Weather conditions and crop stage should be considered during application.');
    doc.moveDown(3);

    // 7. Disclaimer
    doc.fontSize(10).fillColor('#999999').text(
        'Disclaimer: This recommendation is advisory and based on available sensor data and AI models. ' +
        'Please consult with a local agronomist or agricultural expert before making final decisions. ' +
        'MITTI MITRA is not responsible for any crop or financial losses.',
        { align: 'center', width: 500 }
    );

    // Footer
    doc.moveDown(2);
    doc.fontSize(9).fillColor('#CCCCCC').text(
        '─────────────────────────────────────────────────────',
        { align: 'center' }
    );
    doc.fontSize(8).fillColor('#999999').text(
        'Powered by MITTI MITRA - Smart Agriculture System',
        { align: 'center' }
    );

    doc.end();
};

