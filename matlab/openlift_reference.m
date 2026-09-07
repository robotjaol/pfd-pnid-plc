%% OpenLift DED transparent steady-state cross-check
clear; clc;
Pr = 180; Pwh = 22; Phydro = 95;
R = 0.00020 + 0.00010;
N0 = 50; H0 = 105;
frequency = (35:1:60)';
head = H0 .* (frequency ./ N0).^2;
flow = sqrt(max(Pr + head - Phydro - Pwh, 0) ./ R);
result = table(frequency, head, flow);
disp(result(1:5,:));
plot(frequency, flow, 'LineWidth', 1.5); grid on;
xlabel('VFD frequency (Hz)'); ylabel('Equilibrium flow (m^3/d)');
title('OpenLift DED steady-state cross-check');
