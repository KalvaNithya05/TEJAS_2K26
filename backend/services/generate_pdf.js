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
const drawSectionHeader = (title, color = '#1B5E20') => {
    doc.moveDown(0.8);
    doc.fontSize(16).fillColor(color).text(title, { underline: true });
    doc.moveDown(0.4);
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

// 3. Recommendations
if (data.recommendations && data.recommendations.length > 0) {
    data.recommendations.forEach((rec, index) => {
        const isFirst = index === 0;
        const crop = rec.crop;
        const fert = rec.fertilizer;
        const yld = rec.yield;
        const cropName = crop.translated_crop || crop.crop;
        const fertName = fert.translated_name || fert.name;

        // New Page for each recommendation if not first
        // Differentiate colors between top recommendation and others
        const accentColor = isFirst ? '#10B981' : '#6366F1'; // Emerald vs Indigo

        doc.fontSize(14).fillColor(accentColor).text(`Recommendation #${index + 1}: ${cropName.toUpperCase()}`, { underline: true });
        doc.moveDown(0.2);

        // Yield Info
        doc.fontSize(11).fillColor('#000000').text(`Estimated Yield: ${yld.predicted_yield} ${yld.unit} (${yld.season} season)`);
        doc.moveDown(0.3);

        // Fertilizer Section - Using Accent Colors
        doc.fontSize(12).fillColor(accentColor).text('Fertilizer Recommendation: ' + fertName);
        doc.moveDown(0.2);

        if (fert.reasoning && fert.reasoning.length > 0) {
            doc.fontSize(10).fillColor('#1F2937').text('Reasoning:');
            fert.reasoning.forEach(r => {
                doc.fontSize(9).fillColor('#4B5563').text(` • ${r}`, { indent: 15 });
            });
            doc.moveDown(0.1);
        }

        if (fert.application_tips && fert.application_tips.length > 0) {
            doc.fontSize(10).fillColor(accentColor).text('Application Tips:');
            fert.application_tips.forEach(tip => {
                doc.fontSize(9).fillColor('#374151').text(` * ${tip}`, { indent: 15 });
            });
            doc.moveDown(0.1);
        }

        // Crop reasoning
        if (crop.reasoning && crop.reasoning.length > 0) {
            doc.fontSize(10).fillColor('#1F2937').text(`Why ${cropName}?`);
            crop.reasoning.forEach(r => {
                doc.fontSize(9).fillColor('#4B5563').text(` - ${r}`, { indent: 15 });
            });
        }

        doc.moveDown(0.5);
        // Horizontal Separator
        doc.strokeColor('#E5E7EB').lineWidth(0.5).moveTo(50, doc.y).lineTo(550, doc.y).stroke();
        doc.moveDown(0.5);
    });
} else {
    drawSectionHeader('Recommendations');
    doc.fontSize(11).fillColor('#6B7280').text('No recommendations available in the provided data.');
}

// Ensure there's a small break before guidelines if on same page, or move to next
if (doc.y > 550) {
    doc.addPage();
} else {
    doc.moveDown(1);
}

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
