// PDF Generation Script for Node.js
// Called by Python backend to generate PDF reports

const PDFDocument = require('pdfkit');
const fs = require('fs');
const path = require('path');

// Get data file path from command line argument
const dataFilePath = process.argv[2];

if (!dataFilePath) {
    console.error('Error: No data file provided');
    process.exit(1);
}

// Read data from file
let data;
try {
    const rawData = fs.readFileSync(dataFilePath, 'utf8');
    data = JSON.parse(rawData);
} catch (error) {
    console.error('Error reading data file:', error.message);
    process.exit(1);
}

// Create PDF
const outputPath = path.join(__dirname, `report-${Date.now()}.pdf`);
const doc = new PDFDocument({ margin: 50 });
const writeStream = fs.createWriteStream(outputPath);

doc.pipe(writeStream);

// Helper for section headers
const drawSectionHeader = (title) => {
    doc.moveDown(1.5);
    doc.fontSize(16).fillColor('#2E7D32').text(title, { underline: true });
    doc.moveDown(0.5);
};

// 1. Title & Header
doc.fontSize(26).fillColor('#2E7D32').text('MITTI MITRA', { align: 'center' });
doc.fontSize(18).fillColor('#4caf50').text('Crop & Fertilizer Recommendation Report', { align: 'center' });
doc.fontSize(10).fillColor('#666666').text(`Generated: ${new Date().toLocaleString()}`, { align: 'center' });
doc.moveDown(2);

// 2. Soil Analysis Summary
drawSectionHeader('Soil Analysis Summary');
doc.fontSize(11).fillColor('#000000');
doc.text(`Nitrogen (N): ${data.used_params.N} mg/kg`);
doc.text(`Phosphorus (P): ${data.used_params.P} mg/kg`);
doc.text(`Potassium (K): ${data.used_params.K} mg/kg`);
doc.text(`Soil pH: ${data.used_params.ph}`);
doc.text(`Temperature: ${data.used_params.temperature}°C`);
doc.text(`Humidity: ${data.used_params.humidity}%`);
if (data.used_params.moisture) doc.text(`Soil Moisture: ${data.used_params.moisture}%`);
if (data.used_params.soil_type) doc.text(`Soil Type: ${data.used_params.soil_type}`);
doc.moveDown(1);

// 3. Recommended Crops
drawSectionHeader('Recommended Crops');

if (data.crops && data.crops.length > 0) {
    data.crops.forEach((crop, index) => {
        const isBest = index === 0;
        const color = isBest ? '#2E7D32' : '#000000';
        let cropName = crop.translated_crop || crop.crop;

        doc.fontSize(14).fillColor(color).text(
            `${index + 1}. ${cropName.toUpperCase()}`,
            { continued: true }
        );
        doc.fontSize(11).fillColor('#666666').text(
            ` - ${(crop.confidence * 100).toFixed(1)}% confidence`,
            { continued: false }
        );

        if (isBest) {
            doc.fontSize(10).fillColor('#FF9800').text('   ★ Top Recommendation', { indent: 20 });
        }
        doc.moveDown(0.5);
    });
} else {
    doc.fontSize(11).fillColor('#666666').text('No crop recommendations available.');
}

// 4. Yield Prediction (NEW)
if (data.yield_prediction) {
    drawSectionHeader('Estimated Crop Yield');
    const yp = data.yield_prediction;
    doc.fontSize(14).fillColor('#000000').text(`Projected Yield: ${yp.predicted_yield} tons/hectare`, { indent: 20 });
    doc.fontSize(10).fillColor('#666666').text(`Based on optimal conditions for this crop in your region.`, { indent: 20 });
}

// 5. Fertilizer Recommendation
drawSectionHeader('Fertilizer Recommendation');

if (data.fertilizer_recommendation) {
    const fert = data.fertilizer_recommendation;
    let fertName = fert.translated_fertilizer || fert.fertilizer;

    doc.fontSize(14).fillColor('#2E7D32').text('Recommended Fertilizer:', { continued: false });
    doc.fontSize(18).fillColor('#1B5E20').text(fertName, { indent: 20 });
    doc.moveDown(0.3);

    doc.fontSize(11).fillColor('#666666').text(`Confidence: ${(fert.confidence * 100).toFixed(1)}%`, { indent: 20 });
    doc.moveDown(0.5);

    if (fert.reasoning && fert.reasoning.length > 0) {
        doc.fontSize(12).fillColor('#000000').text('Why this fertilizer?');
        doc.fontSize(10).fillColor('#555555');
        fert.reasoning.forEach((reason) => {
            doc.text(`• ${reason}`, { indent: 20 });
            doc.moveDown(0.2);
        });
    }
} else {
    doc.fontSize(11).fillColor('#666666').text('No fertilizer recommendation available.');
}

doc.addPage();

// 6. Application Guidelines (RESTORED)
drawSectionHeader('Application Guidelines');
doc.fontSize(11).fillColor('#555555');
doc.text('1. Apply fertilizer during early morning or late evening to minimize nutrient loss.');
doc.text('2. Ensure soil has adequate moisture before fertilizer application.');
doc.text('3. Follow recommended dosage based on crop stage and field size.');
doc.text('4. Monitor crop response and adjust application as needed.');
doc.text('5. Maintain proper spacing and avoid over-application.');
doc.moveDown(1);

// 7. General Farming Instructions (RESTORED/ENHANCED)
drawSectionHeader('General Farming Instructions');

doc.font('Helvetica-Bold').text('Preparation Phase:');
doc.font('Helvetica').fillColor('#555555');
doc.text('• Clear the field of previous crop residues.', { indent: 15 });
doc.text('• Deep ploughing is recommended to kill soil-borne pathogens.', { indent: 15 });
doc.moveDown(0.5);

doc.font('Helvetica-Bold').fillColor('#000000').text('Sowing Phase:');
doc.font('Helvetica').fillColor('#555555');
doc.text('• Use high-quality certified seeds.', { indent: 15 });
doc.text('• Treat seeds with fungicides before sowing if necessary.', { indent: 15 });
doc.moveDown(0.5);

doc.font('Helvetica-Bold').fillColor('#000000').text('Water Management:');
doc.font('Helvetica').fillColor('#555555');
doc.text('• Avoid water logging.', { indent: 15 });
doc.text('• Critical stages for irrigation: Germination, Tillering, Flowering.', { indent: 15 });
doc.moveDown(1);


// 8. Important Notes
drawSectionHeader('Important Notes');
doc.fontSize(10).fillColor('#555555');
doc.text('• This recommendation is based on current soil analysis and AI predictions.');
doc.text('• Soil conditions may vary across different parts of the field.');
doc.text('• Consider conducting soil tests periodically for best results.');
doc.text('• Weather conditions and crop stage should be considered during application.');
doc.moveDown(3);

// 9. Disclaimer
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

// Wait for PDF to finish writing
writeStream.on('finish', () => {
    console.log(outputPath); // Output the file path for Python to read
    process.exit(0);
});

writeStream.on('error', (error) => {
    console.error('Error writing PDF:', error.message);
    process.exit(1);
});
