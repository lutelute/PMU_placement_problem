%% PMU Optimal Placement Problem - Baldwin et al. 1993
%  "Power System Observability with Minimal Phasor Measurement Placement"
%
%  再現実装:
%    - 観測性ルールによるPMU配置
%    - BILP (二値整数線形計画法) 定式化
%    - シミュレーテッドアニーリング (SA) ヒューリスティック
%    - IEEE 7, 14, 30バステストシステム
%
%  必要なToolbox: Optimization Toolbox (intlinprog)
%  なければSAのみで実行可能

clear; clc; close all;

%% ===== テストシステム定義 =====
systems = {ieee7_bus(), ieee14_bus(), ieee30_bus()};

fprintf('============================================================\n');
fprintf('PMU Optimal Placement Problem\n');
fprintf('Baldwin et al. 1993 - Reproduction\n');
fprintf('============================================================\n');

for s = 1:length(systems)
    sys = systems{s};
    fprintf('\n\n############################################################\n');
    fprintf('# System: %s\n', sys.name);
    fprintf('# Buses: %d, Branches: %d\n', sys.n_bus, size(sys.branches, 1));
    fprintf('############################################################\n');

    % 接続行列の構築
    f = build_connectivity_matrix(sys.n_bus, sys.branches);
    fprintf('\nConnectivity matrix f (first 10x10):\n');
    disp(f(1:min(10,sys.n_bus), 1:min(10,sys.n_bus)));

    % BILP解法
    [pmu_bilp, n_bilp] = solve_bilp(sys);

    % SA解法
    [pmu_sa, n_sa] = solve_sa(sys);

    % 可視化
    figure('Position', [100 100 1200 500]);

    subplot(1, 2, 1);
    visualize_placement(sys, pmu_bilp, ...
        sprintf('%s - BILP (%d PMUs)', sys.name, n_bilp));

    subplot(1, 2, 2);
    visualize_placement(sys, pmu_sa, ...
        sprintf('%s - SA (%d PMUs)', sys.name, n_sa));

    sgtitle(sys.name, 'FontSize', 16, 'FontWeight', 'bold');

    % 保存
    saveas(gcf, sprintf('result_%s.png', strrep(lower(sys.name), ' ', '_')));
end

%% ===== テストシステム定義関数 =====
function sys = ieee7_bus()
    sys.n_bus = 7;
    sys.branches = [
        1 2; 1 3; 2 3; 2 5; 3 4;
        4 5; 4 7; 5 6; 6 7
    ];
    sys.name = 'IEEE 7-bus';
end

function sys = ieee14_bus()
    sys.n_bus = 14;
    sys.branches = [
        1 2; 1 5; 2 3; 2 4; 2 5;
        3 4; 4 5; 4 7; 4 9; 5 6;
        6 11; 6 12; 6 13; 7 8; 7 9;
        9 10; 9 14; 10 11; 12 13; 13 14
    ];
    sys.name = 'IEEE 14-bus';
end

function sys = ieee30_bus()
    sys.n_bus = 30;
    sys.branches = [
        1 2; 1 3; 2 4; 2 5; 2 6;
        3 4; 4 6; 4 12; 5 7; 6 7;
        6 8; 6 9; 6 10; 6 28; 8 28;
        9 10; 9 11; 10 17; 10 20; 10 21;
        10 22; 12 13; 12 14; 12 15; 12 16;
        14 15; 15 18; 15 23; 16 17; 18 19;
        19 20; 21 22; 22 24; 23 24; 24 25;
        25 26; 25 27; 27 28; 27 29; 27 30;
        29 30
    ];
    sys.name = 'IEEE 30-bus';
end

%% ===== 接続行列構築 =====
function f = build_connectivity_matrix(n_bus, branches)
    % f(i,j) = 1 if bus j can observe bus i
    A = zeros(n_bus);
    for k = 1:size(branches, 1)
        i = branches(k, 1);
        j = branches(k, 2);
        A(i, j) = 1;
        A(j, i) = 1;
    end
    f = A + eye(n_bus);
end

%% ===== 観測性チェック =====
function [is_obs, observed, depth] = check_observability(pmu_buses, n_bus, branches)
    f = build_connectivity_matrix(n_bus, branches);
    x = zeros(n_bus, 1);
    x(pmu_buses) = 1;
    depth = f * x;
    observed = find(depth >= 1);
    is_obs = (length(observed) == n_bus);
end

%% ===== BILP解法 =====
function [pmu_buses, n_pmu] = solve_bilp(sys)
    n = sys.n_bus;
    f_mat = build_connectivity_matrix(n, sys.branches);

    fprintf('\n--- BILP Solution for %s ---\n', sys.name);

    % intlinprogが利用可能か確認
    if exist('intlinprog', 'file')
        % min c'x s.t. A*x <= b, x binary
        c = ones(n, 1);            % 目的関数: PMU数最小化
        A = -f_mat;                % -f*x <= -1 (各バスが少なくとも1つのPMUで観測)
        b = -ones(n, 1);
        lb = zeros(n, 1);
        ub = ones(n, 1);
        intcon = 1:n;              % 全変数が整数

        options = optimoptions('intlinprog', 'Display', 'off');
        x = intlinprog(c, intcon, A, b, [], [], lb, ub, options);
        x = round(x);
    else
        fprintf('  intlinprog not available. Using exhaustive search...\n');
        x = exhaustive_search(n, f_mat);
    end

    pmu_buses = find(x == 1)';
    n_pmu = length(pmu_buses);

    [is_obs, ~, depth] = check_observability(pmu_buses, n, sys.branches);
    fprintf('  Number of PMUs: %d\n', n_pmu);
    fprintf('  PMU locations: [%s]\n', num2str(pmu_buses));
    fprintf('  Complete observability: %d\n', is_obs);
    fprintf('  Observability depth: [%s]\n', num2str(depth'));
end

function x_best = exhaustive_search(n, f_mat)
    % 小規模系統用の全探索
    x_best = ones(n, 1);
    best_cost = n;

    for k = 1:n
        combos = nchoosek(1:n, k);
        for c = 1:size(combos, 1)
            x = zeros(n, 1);
            x(combos(c, :)) = 1;
            if all(f_mat * x >= 1)
                if k < best_cost
                    best_cost = k;
                    x_best = x;
                end
                return;  % kの昇順なので最初に見つかったのが最適
            end
        end
    end
end

%% ===== シミュレーテッドアニーリング =====
function [pmu_buses, n_pmu] = solve_sa(sys)
    n = sys.n_bus;
    f_mat = build_connectivity_matrix(n, sys.branches);

    fprintf('\n--- SA Solution for %s ---\n', sys.name);

    best_k = n;
    best_x = ones(n, 1);

    % 二分探索でPMU数を決定
    lo = 1; hi = n;
    n_trials = 10;

    while lo <= hi
        mid = floor((lo + hi) / 2);
        found = false;

        for trial = 1:n_trials
            result = sa_feasibility(n, f_mat, mid);
            if ~isempty(result)
                found = true;
                if mid < best_k
                    best_k = mid;
                    best_x = result;
                end
                break;
            end
        end

        if found
            hi = mid - 1;
        else
            lo = mid + 1;
        end
    end

    pmu_buses = find(best_x == 1)';
    n_pmu = length(pmu_buses);

    [is_obs, ~, depth] = check_observability(pmu_buses, n, sys.branches);
    fprintf('  Number of PMUs: %d\n', n_pmu);
    fprintf('  PMU locations: [%s]\n', num2str(pmu_buses));
    fprintf('  Complete observability: %d\n', is_obs);
    fprintf('  Observability depth: [%s]\n', num2str(depth'));
end

function x = sa_feasibility(n, f_mat, k)
    % k個のPMUで完全観測性が達成可能か、SAで探索
    x = zeros(n, 1);
    indices = randperm(n, k);
    x(indices) = 1;

    cost = sum(f_mat * x < 1);
    if cost == 0
        return;
    end

    best_x = x;
    best_cost = cost;
    T = 10.0;
    T_min = 0.01;
    alpha = 0.995;
    max_iter = 5000;

    for iter = 1:max_iter
        if T < T_min
            break;
        end

        pmu_idx = find(x == 1);
        non_pmu_idx = find(x == 0);

        if isempty(pmu_idx) || isempty(non_pmu_idx)
            break;
        end

        % 近傍: PMUを1つ移動
        remove = pmu_idx(randi(length(pmu_idx)));
        add = non_pmu_idx(randi(length(non_pmu_idx)));

        x_new = x;
        x_new(remove) = 0;
        x_new(add) = 1;

        new_cost = sum(f_mat * x_new < 1);
        delta = new_cost - cost;

        if delta <= 0 || rand() < exp(-delta / T)
            x = x_new;
            cost = new_cost;

            if cost < best_cost
                best_x = x;
                best_cost = cost;
            end

            if best_cost == 0
                x = best_x;
                return;
            end
        end

        T = T * alpha;
    end

    if best_cost == 0
        x = best_x;
    else
        x = [];  % 失敗
    end
end

%% ===== 可視化 =====
function visualize_placement(sys, pmu_buses, plot_title)
    n = sys.n_bus;
    branches = sys.branches;

    % グラフ構築
    G = graph(branches(:,1), branches(:,2));

    % バス位置
    pos = get_bus_positions(sys.name, n);

    % 観測性チェック
    [~, ~, depth] = check_observability(pmu_buses, n, branches);

    % ノード色
    colors = zeros(n, 3);
    for i = 1:n
        if ismember(i, pmu_buses)
            colors(i, :) = [0.906 0.298 0.235];  % Red
        elseif depth(i) >= 1
            colors(i, :) = [0.180 0.800 0.443];  % Green
        else
            colors(i, :) = [0.584 0.647 0.651];  % Grey
        end
    end

    % 描画
    if ~isempty(pos)
        h = plot(G, 'XData', pos(:,1), 'YData', pos(:,2));
    else
        h = plot(G, 'Layout', 'force');
    end

    h.NodeColor = colors;
    h.MarkerSize = 12;
    h.LineWidth = 2;
    h.EdgeColor = [0.5 0.5 0.5];
    h.NodeFontSize = 10;
    h.NodeFontWeight = 'bold';

    % ラベル: バス番号 + 深度
    labels = cell(n, 1);
    for i = 1:n
        labels{i} = sprintf('%d(d=%d)', i, depth(i));
    end
    h.NodeLabel = labels;

    title(plot_title, 'FontSize', 12);
    axis off;
end

function pos = get_bus_positions(name, n)
    pos = [];
    if contains(name, '14')
        pos = [
            0 4; 2 4; 4 3; 3 2;
            1 2; 4 1; 5 2; 6 2.5;
            5 0.5; 5 -0.5; 4.5 -0.5;
            3.5 0; 4 -0.5; 5.5 -0.5
        ];
    elseif contains(name, '7')
        pos = [
            0 2; 1 3; 1 1;
            2 1; 2 3; 3 2; 3 0.5
        ];
    end
end
